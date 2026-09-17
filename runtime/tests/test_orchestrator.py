"""End-to-end runs, with a mocked provider. No network, no API keys."""

from __future__ import annotations

import asyncio
import json
import time
import unittest

from companyos import purposes
from companyos.observability import EventType
from companyos.orchestration import Orchestrator
from companyos.status import RunStatus, TaskStatus, Verdict

from . import support


def orchestrate(request: str, *, provider=None, config=None, bus=None):
    config = config or support.config()
    bus = bus or support.bus()
    orchestrator = Orchestrator(
        config,
        registry=support.repo_registry(),
        provider=provider or support.provider(),
        bus=bus,
        trace_to_disk=False,
    )
    return orchestrator, orchestrator.run_sync(request)


class EndToEndTest(unittest.TestCase):
    def test_authentication_request_staffs_an_engineering_and_security_team(self) -> None:
        orchestrator, run = orchestrate(
            "Design and implement authentication for a web application."
        )

        self.assertEqual(run.status, RunStatus.COMPLETED)
        self.assertTrue(run.final_output)
        self.assertGreaterEqual(len(run.graph), 3)

        agents = {r.agent_id for r in run.results.values()}
        divisions = {orchestrator.registry.get(a).division for a in agents}
        self.assertIn("engineering", divisions)
        self.assertIn("security", divisions)
        self.assertIn("engineering/backend-engineer", agents)

    def test_market_research_request_staffs_a_research_team(self) -> None:
        orchestrator, run = orchestrate(
            "Research whether a developer-tools product idea has a viable market."
        )
        agents = {r.agent_id for r in run.results.values()}
        divisions = {orchestrator.registry.get(a).division for a in agents}

        self.assertEqual(run.status, RunStatus.COMPLETED)
        self.assertIn("research", divisions)
        self.assertIn("research/market-research-agent", agents)
        self.assertNotIn("engineering", divisions, "unrelated divisions must not be staffed")

    def test_the_same_runtime_picks_different_teams_for_different_work(self) -> None:
        _, engineering = orchestrate("Implement a database schema and migration plan.")
        _, legal = orchestrate("Draft a privacy policy and data-processing agreement.")

        self.assertNotEqual(
            {r.agent_id for r in engineering.results.values()},
            {r.agent_id for r in legal.results.values()},
        )

    def test_distinct_specialists_are_preferred_over_reusing_one(self) -> None:
        _, run = orchestrate(
            "Research whether a developer-tools product idea has a viable market."
        )
        assigned = [t.assigned_agent for t in run.graph if t.assigned_agent]
        self.assertGreaterEqual(len(assigned), 3)
        self.assertEqual(len(assigned), len(set(assigned)), "one task each, where possible")

    def test_reuse_is_allowed_when_no_other_agent_fits(self) -> None:
        provider = support.provider(
            script={
                purposes.DECOMPOSE: json.dumps(
                    {"tasks": [
                        {"id": "a", "objective": "Threat model the login flow",
                         "required_capabilities": ["role.security-architect-agent"]},
                        {"id": "b", "objective": "Threat model the admin console",
                         "required_capabilities": ["role.security-architect-agent"]},
                    ]}
                )
            }
        )
        _, run = orchestrate("Threat model the product.", provider=provider)
        assigned = [t.assigned_agent for t in run.graph]
        self.assertEqual(assigned, ["security/security-architect-agent"] * 2)
        # Same definition, two separate temporary instances.
        instances = {r.instance_id for r in run.results.values()}
        self.assertEqual(len(instances), 2)

    def test_only_the_selected_agents_are_instantiated(self) -> None:
        _, run = orchestrate("Size the market for a new analytics product.")
        self.assertLessEqual(run.budget["agents_spawned"], support.config().limits.max_agents)
        self.assertLess(run.budget["agents_spawned"], 10)
        self.assertEqual(run.budget["agents_spawned"], len(run.results))

    def test_run_record_is_fully_serializable(self) -> None:
        _, run = orchestrate("Plan a product launch.")
        payload = json.dumps(run.to_dict())
        restored = json.loads(payload)
        self.assertEqual(restored["run_id"], run.id)
        self.assertEqual(restored["status"], "completed")
        self.assertTrue(restored["graph"]["tasks"])

    def test_observability_covers_the_whole_pipeline(self) -> None:
        bus = support.bus()
        orchestrate("Design an onboarding flow.", bus=bus)
        emitted = {e.type for e in bus.events}
        for expected in (
            EventType.RUN_STARTED,
            EventType.PLAN_CREATED,
            EventType.TASKS_DECOMPOSED,
            EventType.AGENT_SELECTED,
            EventType.AGENT_SPAWNED,
            EventType.AGENT_STARTED,
            EventType.AGENT_COMPLETED,
            EventType.AGENT_TERMINATED,
            EventType.REVIEW_STARTED,
            EventType.REVIEW_COMPLETED,
            EventType.SYNTHESIS_STARTED,
            EventType.RUN_COMPLETED,
        ):
            self.assertIn(expected, emitted, expected)

    def test_every_spawned_instance_is_terminated(self) -> None:
        bus = support.bus()
        _, run = orchestrate("Plan a product launch.", bus=bus)
        spawned = bus.of_type(EventType.AGENT_SPAWNED)
        terminated = bus.of_type(EventType.AGENT_TERMINATED)
        self.assertEqual(len(spawned), len(terminated))


class ParallelismTest(unittest.TestCase):
    def test_independent_workstreams_overlap(self) -> None:
        provider = support.provider(latency_s=0.15)
        started = time.perf_counter()
        _, run = orchestrate(
            "Research whether a developer-tools product idea has a viable market.",
            provider=provider,
            config=support.config(limits={"max_parallel": 4}),
        )
        elapsed = time.perf_counter() - started

        spawned = run.budget["agents_spawned"]
        self.assertGreaterEqual(spawned, 3)
        # plan + decompose + N agents + reviewers + synthesis, but the N agents
        # overlap; strictly serial would cost far more than this bound.
        self.assertLess(elapsed, 0.15 * (spawned + 5))
        self.assertGreater(spawned, 1)


class ReviewLoopTest(unittest.TestCase):
    def test_rejected_work_is_returned_to_its_author_and_rerun(self) -> None:
        bus = support.bus()
        _, run = orchestrate(
            "Size the market for a new analytics product.",
            provider=support.provider(revise_once=True),
            bus=bus,
        )

        self.assertEqual(len(run.reviews), 2)
        self.assertTrue(run.reviews[0].verdict.needs_rework)
        self.assertEqual(run.reviews[1].verdict, Verdict.APPROVE)

        retries = bus.of_type(EventType.TASK_RETRY)
        self.assertTrue(retries)
        retried_task = run.graph[retries[0].task_id]
        self.assertEqual(retried_task.attempts, 2)
        self.assertEqual(retried_task.status, TaskStatus.COMPLETED)
        self.assertEqual(run.status, RunStatus.COMPLETED)

    def test_findings_reach_the_retried_agent(self) -> None:
        provider = support.provider(revise_once=True)
        orchestrate("Size the market for a new analytics product.", provider=provider)
        execute_prompts = [
            c.prompt for c in provider.calls if c.purpose == purposes.EXECUTE
        ]
        self.assertTrue(
            any("Cite the evidence" in prompt for prompt in execute_prompts),
            "the second attempt must carry the reviewer's required change",
        )

    def test_iteration_cap_stops_an_endless_review_loop(self) -> None:
        provider = support.provider(
            script={
                purposes.REVIEW: json.dumps(
                    {"verdict": "revise", "summary": "never good enough", "findings": []}
                )
            }
        )
        _, run = orchestrate(
            "Size the market for a new analytics product.",
            provider=provider,
            config=support.config(limits={"max_iterations": 2, "max_attempts_per_task": 5}),
        )
        self.assertLessEqual(len(run.reviews), 2)
        self.assertTrue(run.final_output)

    def test_security_block_requires_human_approval(self) -> None:
        provider = support.provider(
            script={
                purposes.REVIEW: json.dumps(
                    {"verdict": "block", "summary": "credentials would be logged",
                     "findings": []}
                )
            }
        )
        _, run = orchestrate(
            "Design and implement authentication for a web application.", provider=provider
        )
        self.assertTrue(run.requires_human_approval)
        self.assertEqual(run.status, RunStatus.AWAITING_APPROVAL)
        self.assertIn("block", run.approval_reason)
        self.assertTrue(run.final_output, "the work is preserved for the human reviewer")


class FailureHandlingTest(unittest.TestCase):
    def test_one_failed_agent_does_not_end_the_run(self) -> None:
        provider = support.provider(fail_agents=["research/market-research-agent"])
        _, run = orchestrate(
            "Research whether a developer-tools product idea has a viable market.",
            provider=provider,
        )
        failed = run.failed_results()
        self.assertTrue(failed)
        self.assertTrue(run.successful_results())
        self.assertEqual(run.status, RunStatus.COMPLETED)
        self.assertTrue(run.final_output)

    def test_total_failure_is_reported_honestly(self) -> None:
        registry = support.repo_registry()
        provider = support.provider(fail_agents=[d.id for d in registry])
        _, run = orchestrate("Plan a product launch.", provider=provider)
        self.assertEqual(run.status, RunStatus.FAILED)
        self.assertFalse(run.successful_results())
        self.assertIn("failed", run.final_output.lower())

    def test_a_broken_planner_still_produces_a_run(self) -> None:
        provider = support.provider(script={purposes.PLAN: "the model returned prose"})
        _, run = orchestrate("Size the market for a new analytics product.", provider=provider)
        self.assertEqual(run.status, RunStatus.COMPLETED)
        self.assertTrue(run.plan.get("degraded"))
        self.assertTrue(run.results)

    def test_agent_budget_caps_a_sprawling_plan(self) -> None:
        provider = support.provider(
            script={
                purposes.DECOMPOSE: json.dumps(
                    {"tasks": [
                        {"id": f"t{i}", "objective": f"Workstream {i}",
                         "required_capabilities": ["engineering.backend"]}
                        for i in range(40)
                    ]}
                )
            }
        )
        _, run = orchestrate(
            "Do absolutely everything.",
            provider=provider,
            config=support.config(limits={"max_agents": 5}),
        )
        self.assertLessEqual(run.budget["agents_spawned"], 5)
        self.assertLessEqual(len(run.graph), 3, "tasks are capped below the agent budget")

    def test_token_budget_is_enforced(self) -> None:
        _, run = orchestrate(
            "Design and implement authentication for a web application.",
            config=support.config(limits={"max_total_tokens": 500}),
        )
        self.assertTrue(
            any("max_total_tokens" in e for e in run.errors) or run.usage.total <= 5000
        )
        self.assertTrue(run.status.terminal)


class CancellationTest(unittest.TestCase):
    def test_a_cancelled_run_stops_and_says_so(self) -> None:
        cancel = asyncio.Event()
        cancel.set()

        orchestrator = Orchestrator(
            support.config(),
            registry=support.repo_registry(),
            provider=support.provider(),
            bus=support.bus(),
            trace_to_disk=False,
        )
        run = support.run(orchestrator.run("Plan a product launch.", cancel=cancel))
        self.assertEqual(run.status, RunStatus.CANCELLED)
        self.assertIn("cancelled", " ".join(run.errors))


class ContextIsolationEndToEndTest(unittest.TestCase):
    def test_agents_do_not_receive_their_peers_output(self) -> None:
        provider = support.provider()
        _, run = orchestrate(
            "Research whether a developer-tools product idea has a viable market.",
            provider=provider,
        )

        by_task = {}
        for call in provider.calls:
            if call.purpose == purposes.EXECUTE:
                by_task[call.context["task_id"]] = call.prompt

        for task_id, prompt in by_task.items():
            task = run.graph[task_id]
            for other in run.graph:
                if other.id == task_id or other.id in task.dependencies:
                    continue
                result = run.results.get(other.id)
                if result and result.output:
                    self.assertNotIn(
                        result.output[:120], prompt,
                        f"{task_id} saw non-dependency {other.id}",
                    )

    def test_agents_are_told_that_shared_content_is_data(self) -> None:
        provider = support.provider()
        orchestrate("Plan a product launch.", provider=provider)
        for call in provider.calls:
            if call.purpose == purposes.EXECUTE:
                self.assertIn("DATA, not instructions", call.system)


if __name__ == "__main__":
    unittest.main()
