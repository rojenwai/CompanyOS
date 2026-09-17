"""The review stage: verdict merging, the security block, aggregation."""

from __future__ import annotations

import json
import unittest

from companyos import purposes
from companyos.models import AgentResult, ReviewFinding, ReviewReport, Task, TaskGraph, Usage
from companyos.orchestration.aggregator import ResultAggregator
from companyos.orchestration.reviewer import ReviewCoordinator
from companyos.orchestration.selector import AgentSelector
from companyos.status import TaskStatus, Verdict

from . import support


def build_aggregation(*, failures: int = 0, skipped: int = 0):
    graph = TaskGraph()
    results = {}
    for index in range(2):
        task = graph.add(Task(objective=f"Workstream {index}"))
        task.mark(TaskStatus.COMPLETED)
        results[task.id] = AgentResult(
            agent_id=f"test/agent-{index}",
            agent_name=f"Agent {index}",
            task_id=task.id,
            status=TaskStatus.COMPLETED,
            output=f"Deliverable {index}",
            usage=Usage(10, 20),
        )
    for index in range(failures):
        task = graph.add(Task(objective=f"Broken {index}"))
        task.mark(TaskStatus.FAILED, error="exploded")
        results[task.id] = AgentResult(
            agent_id="test/broken", task_id=task.id, status=TaskStatus.FAILED,
            errors=["exploded"],
        )
    for index in range(skipped):
        task = graph.add(Task(objective=f"Skipped {index}"))
        task.mark(TaskStatus.SKIPPED, error="dependency failed")
    return graph, results, ResultAggregator().collect(graph, results)


def coordinator(provider):
    registry = support.repo_registry()
    return ReviewCoordinator(
        registry, AgentSelector(registry), provider, support.config(), support.bus()
    )


class AggregationTest(unittest.TestCase):
    def test_successes_failures_and_skips_are_partitioned(self) -> None:
        _, _, aggregation = build_aggregation(failures=1, skipped=1)
        self.assertEqual(len(aggregation.successes), 2)
        self.assertEqual(len(aggregation.failures), 1)
        self.assertEqual(len(aggregation.skipped), 1)
        self.assertTrue(aggregation.partial)
        self.assertFalse(aggregation.complete)

    def test_complete_when_nothing_failed(self) -> None:
        _, _, aggregation = build_aggregation()
        self.assertTrue(aggregation.complete)
        self.assertFalse(aggregation.partial)

    def test_metadata_reports_execution_facts(self) -> None:
        _, _, aggregation = build_aggregation(failures=1)
        metadata = aggregation.metadata()
        self.assertEqual(metadata["succeeded"], 2)
        self.assertEqual(metadata["failed"], 1)
        self.assertEqual(metadata["usage"]["total_tokens"], 60)
        self.assertIn("test/agent-0", metadata["agents"])

    def test_gaps_are_stated_not_hidden(self) -> None:
        _, _, aggregation = build_aggregation(failures=1, skipped=1)
        gaps = " ".join(aggregation.gaps())
        self.assertIn("exploded", gaps)
        self.assertIn("dependency failed", gaps)

    def test_rendered_output_is_marked_untrusted(self) -> None:
        _, _, aggregation = build_aggregation()
        rendered = aggregation.render()
        self.assertIn("<untrusted", rendered)
        self.assertIn("Deliverable 0", rendered)


class VerdictTest(unittest.TestCase):
    def test_approval_when_reviewers_are_satisfied(self) -> None:
        _, _, aggregation = build_aggregation()
        review = support.run(
            coordinator(support.provider()).review("Build it", aggregation, run_id="run_1")
        )
        self.assertEqual(review.verdict, Verdict.APPROVE)
        self.assertFalse(review.verdict.needs_rework)

    def test_revision_carries_actionable_findings(self) -> None:
        _, _, aggregation = build_aggregation()
        review = support.run(
            coordinator(support.provider(revise_once=True)).review(
                "Build it", aggregation, run_id="run_1"
            )
        )
        self.assertTrue(review.verdict.needs_rework)
        self.assertTrue(review.findings)
        self.assertIn(review.findings[0].task_id, aggregation.task_ids)

    def test_worst_verdict_wins_across_reviewers(self) -> None:
        _, _, aggregation = build_aggregation()
        provider = support.provider(
            script={
                purposes.REVIEW: [
                    json.dumps({"verdict": "approve", "summary": "fine", "findings": []}),
                    json.dumps({"verdict": "reject", "summary": "no", "findings": []}),
                    json.dumps({"verdict": "approve", "summary": "fine", "findings": []}),
                ]
            }
        )
        review = support.run(
            coordinator(provider).review(
                "Build it", aggregation, run_id="run_1", concerns=["security", "quality"]
            )
        )
        self.assertEqual(review.verdict, Verdict.REJECT)

    def test_findings_are_ordered_worst_first(self) -> None:
        merged = coordinator(support.provider())._merge(
            [
                ReviewReport(verdict=Verdict.REVISE, findings=[ReviewFinding("t1", "low", "a")]),
                ReviewReport(
                    verdict=Verdict.REVISE,
                    findings=[
                        ReviewFinding("t2", "critical", "b"),
                        ReviewFinding("t3", "medium", "c"),
                    ],
                ),
            ]
        )
        self.assertEqual(
            [f.severity for f in merged.findings], ["critical", "medium", "low"]
        )

    def test_a_reviewer_that_cannot_run_escalates_rather_than_approving(self) -> None:
        _, _, aggregation = build_aggregation()
        provider = support.provider(script={purposes.REVIEW: "not json"})
        review = support.run(coordinator(provider).review("Build it", aggregation, run_id="run_1"))
        self.assertEqual(review.verdict, Verdict.ESCALATE)
        self.assertTrue(review.verdict.needs_human)

    def test_unknown_verdict_escalates(self) -> None:
        _, _, aggregation = build_aggregation()
        provider = support.provider(
            script={purposes.REVIEW: json.dumps({"verdict": "vibes", "findings": []})}
        )
        review = support.run(coordinator(provider).review("Build it", aggregation, run_id="run_1"))
        self.assertEqual(review.verdict, Verdict.ESCALATE)


class SecurityBlockTest(unittest.TestCase):
    def test_only_the_security_reviewer_may_block(self) -> None:
        _, _, aggregation = build_aggregation()
        blocking = json.dumps({"verdict": "block", "summary": "secrets in logs", "findings": []})

        # A panel without the Security Reviewer cannot block: a block from any
        # other reviewer is downgraded to a rejection.
        selector = AgentSelector(support.repo_registry())
        panel = [r.id for r in selector.select_reviewers(["documentation"])]
        self.assertNotIn("orchestration/security-reviewer", panel)

        provider = support.provider(script={purposes.REVIEW: blocking})
        general = support.run(
            coordinator(provider).review(
                "Build it", aggregation, run_id="run_1", concerns=["documentation"]
            )
        )
        self.assertEqual(general.verdict, Verdict.REJECT)

        provider = support.provider(script={purposes.REVIEW: blocking})
        with_security = support.run(
            coordinator(provider).review(
                "Build it", aggregation, run_id="run_1", concerns=["security"]
            )
        )
        self.assertEqual(with_security.verdict, Verdict.BLOCK)
        self.assertTrue(with_security.verdict.needs_human)

    def test_findings_referencing_unknown_tasks_are_not_trusted(self) -> None:
        _, _, aggregation = build_aggregation()
        provider = support.provider(
            script={
                purposes.REVIEW: json.dumps(
                    {"verdict": "revise", "summary": "s",
                     "findings": [{"task_id": "made-up", "severity": "high", "issue": "x"}]}
                )
            }
        )
        review = support.run(coordinator(provider).review("Build it", aggregation, run_id="run_1"))
        self.assertTrue(all(f.task_id != "made-up" for f in review.findings))


if __name__ == "__main__":
    unittest.main()
