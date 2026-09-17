"""Capability-based agent selection."""

from __future__ import annotations

import unittest

from companyos.errors import NoSuitableAgentError
from companyos.orchestration.selector import AgentSelector

from . import support


class SelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()
        self.selector = AgentSelector(self.registry)

    def test_each_capability_picks_its_own_specialist(self) -> None:
        expected = {
            "engineering.database": "engineering/database-engineer",
            "engineering.backend": "engineering/backend-engineer",
            "engineering.frontend": "engineering/frontend-engineer",
            "security.threat-modeling": "security/security-architect-agent",
            "security.pentest": "security/penetration-testing-agent",
            "research.market": "research/market-research-agent",
            "research.competitive": "research/competitor-analysis-agent",
            "research.problem": "research/problem-discovery-agent",
            "finance.planning": "finance/financial-planning-agent",
            "legal.privacy": "legal/privacy-terms-agent",
            "design.accessibility": "design/accessibility-agent",
            "data.governance": "data/data-governance-agent",
        }
        for capability, agent_id in expected.items():
            with self.subTest(capability=capability):
                self.assertEqual(self.selector.select([capability]).agent_id, agent_id)

    def test_selection_beats_incidental_mentions_by_a_margin(self) -> None:
        ranked = self.selector.rank(["engineering.database"], "design the user schema")
        self.assertEqual(ranked[0].agent_id, "engineering/database-engineer")
        self.assertGreater(ranked[0].score - ranked[1].score, 1.0)

    def test_delegators_are_excluded_from_executable_work(self) -> None:
        candidate = self.selector.select(["engineering.architecture"], "choose the stack")
        self.assertTrue(candidate.definition.can_execute_independently)
        self.assertNotEqual(candidate.agent_id, "executive/cto-agent")

    def test_delegators_never_appear_in_executable_ranking(self) -> None:
        ranked = self.selector.rank(["executive.direction"], "set the company objective")
        self.assertTrue(ranked)
        self.assertTrue(all(c.definition.can_execute_independently for c in ranked))

    def test_delegators_are_visible_when_execution_is_not_required(self) -> None:
        ranked = self.selector.rank(
            ["executive.direction"], "set the company objective", executable_only=False
        )
        self.assertIn(
            "orchestration/ceo-agent", [c.agent_id for c in ranked]
        )

    def test_no_hardcoded_routing_table(self) -> None:
        """Selection is driven by tags, not by the task's literal wording."""
        by_capability = self.selector.select(["security.threat-modeling"], "")
        by_prose = self.selector.select([], "build a STRIDE threat model of the login flow")
        self.assertEqual(by_capability.agent_id, "security/security-architect-agent")
        self.assertEqual(by_prose.definition.division, "security")

    def test_unmatchable_capability_raises_rather_than_guessing(self) -> None:
        selector = AgentSelector(self.registry, threshold=50.0)
        with self.assertRaises(NoSuitableAgentError):
            selector.select(["astrology.natal-charts"], "read the stars")

    def test_exclusion_picks_the_next_best(self) -> None:
        first = self.selector.select(["engineering.database"])
        second = self.selector.select(["engineering.database"], exclude={first.agent_id})
        self.assertNotEqual(first.agent_id, second.agent_id)
        self.assertLessEqual(second.score, first.score)

    def test_reasons_are_reported_for_auditability(self) -> None:
        candidate = self.selector.select(["security.threat-modeling"], "threat model")
        self.assertIn("exact", candidate.reasons)
        self.assertIn("security.threat-modeling", candidate.matched)


class TeamSelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.selector = AgentSelector(support.repo_registry())

    def test_one_agent_per_capability_group_without_repeats(self) -> None:
        team = self.selector.select_team(
            [["security.controls"], ["engineering.backend"], ["engineering.database"]],
            "design and implement authentication",
        )
        ids = [c.agent_id for c in team]
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(set(ids)), 3)
        self.assertIn("engineering/database-engineer", ids)

    def test_team_is_capped(self) -> None:
        groups = [[c] for c in ("research.market", "research.competitive", "finance.planning")]
        self.assertEqual(len(self.selector.select_team(groups, "", limit=2)), 2)

    def test_unmatchable_groups_are_skipped_not_fatal(self) -> None:
        selector = AgentSelector(support.repo_registry(), threshold=4.0)
        team = selector.select_team([["engineering.backend"], ["astrology.natal-charts"]], "")
        self.assertEqual(len(team), 1)


class ReviewerSelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.selector = AgentSelector(support.repo_registry())

    def test_general_reviewer_is_always_included(self) -> None:
        ids = [r.id for r in self.selector.select_reviewers([])]
        self.assertIn("orchestration/reviewer", ids)

    def test_security_concern_adds_the_security_reviewer(self) -> None:
        ids = [r.id for r in self.selector.select_reviewers(["security"])]
        self.assertIn("orchestration/security-reviewer", ids)

    def test_quality_concern_adds_the_qa_reviewer(self) -> None:
        ids = [r.id for r in self.selector.select_reviewers(["quality"])]
        self.assertIn("orchestration/qa-reviewer", ids)


if __name__ == "__main__":
    unittest.main()
