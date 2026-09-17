"""Agent discovery and spec parsing."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from companyos.errors import AgentNotFoundError, RegistryError
from companyos.registry import AgentRegistry, parse_agent_spec
from companyos.registry.definition import AgentKind

from . import support


class DiscoveryTest(unittest.TestCase):
    """Discovery over the repository's real specs."""

    def setUp(self) -> None:
        self.registry = support.repo_registry()

    def test_discovers_every_documented_agent(self) -> None:
        # ai/README.md advertises 107 specs; the kernel adds the spec-bearing
        # orchestration agents on top.
        self.assertGreaterEqual(len(self.registry), 107)

    def test_kernel_agents_are_discovered(self) -> None:
        for agent_id in (
            "orchestration/ceo-agent",
            "orchestration/planner",
            "orchestration/task-decomposer",
            "orchestration/reviewer",
            "orchestration/security-reviewer",
        ):
            self.assertIn(agent_id, self.registry, agent_id)

    def test_prose_kernel_documents_are_not_agents(self) -> None:
        # approval-engine.md and friends carry no numbered sections.
        for not_an_agent in (
            "orchestration/approval-engine",
            "orchestration/task-routing",
            "orchestration/execution-lifecycle",
        ):
            self.assertNotIn(not_an_agent, self.registry)

    def test_divisions_match_the_handbook_folders(self) -> None:
        for division in ("engineering", "security", "research", "post-launch", "ai-engineering"):
            self.assertIn(division, self.registry.divisions)
        # No slugified prose like "post-launch---maintenance".
        self.assertFalse([d for d in self.registry.divisions if "--" in d])

    def test_specs_are_referenced_not_copied(self) -> None:
        definition = self.registry.get("engineering/backend-engineer")
        source = support.REPO_ROOT / definition.source_path
        self.assertTrue(source.is_file())
        self.assertIn("Backend Engineer", source.read_text(encoding="utf-8"))

    def test_all_eleven_sections_are_parsed(self) -> None:
        definition = self.registry.get("engineering/backend-engineer")
        self.assertEqual(sorted(definition.sections), list(range(1, 12)))


class ParsingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()

    def test_inline_division_dialect(self) -> None:
        definition = self.registry.get("engineering/backend-engineer")
        self.assertEqual(definition.division, "engineering")
        self.assertEqual(definition.reports_to, "Software Architect")

    def test_spec_without_a_division_line_falls_back_to_its_folder(self) -> None:
        definition = self.registry.get("security/security-architect-agent")
        self.assertEqual(definition.division, "security")
        self.assertEqual(definition.kind, AgentKind.SPECIALIST)

    def test_capabilities_are_extracted_from_spec_text(self) -> None:
        definition = self.registry.get("security/security-architect-agent")
        self.assertIn("security.threat-modeling", definition.capabilities)
        self.assertIn("division.security", definition.capabilities)
        self.assertIn("role.security-architect-agent", definition.capabilities)

    def test_capability_depth_reflects_the_spec(self) -> None:
        database = self.registry.get("engineering/database-engineer")
        api = self.registry.get("engineering/api-architect")
        self.assertGreater(
            database.capability_scores["engineering.database"],
            api.capability_scores.get("engineering.database", 0),
        )

    def test_tools_are_mapped_and_prohibitions_respected(self) -> None:
        backend = self.registry.get("engineering/backend-engineer")
        self.assertIn("run_checks", backend.tools)
        reviewer = self.registry.get("orchestration/reviewer")
        self.assertIn("read_spec", reviewer.tools)

    def test_delegators_cannot_execute(self) -> None:
        self.assertFalse(self.registry.get("executive/cto-agent").can_execute_independently)
        self.assertFalse(self.registry.get("orchestration/ceo-agent").can_execute_independently)
        self.assertTrue(self.registry.get("engineering/backend-engineer").can_execute_independently)

    def test_reviewers_declare_their_concerns(self) -> None:
        security = self.registry.get("orchestration/security-reviewer")
        self.assertEqual(security.kind, AgentKind.REVIEWER)
        self.assertIn("security", security.reviews_for)
        self.assertIn("quality", self.registry.get("orchestration/qa-reviewer").reviews_for)

    def test_non_agent_markdown_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prose.md"
            path.write_text("# Just prose\n\nNo numbered sections here.\n", encoding="utf-8")
            with self.assertRaises(RegistryError):
                parse_agent_spec(path)


class HierarchyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()

    def test_executives_declare_the_divisions_they_supervise(self) -> None:
        cto = self.registry.get("executive/cto-agent")
        self.assertIn("engineering", cto.supervises)
        self.assertIn("devops", cto.supervises)

    def test_supervisor_chain_comes_from_the_specs(self) -> None:
        backend = self.registry.get("engineering/backend-engineer")
        self.assertEqual(
            self.registry.supervisor_for(backend), "engineering/software-architect"
        )
        security = self.registry.get("security/security-architect-agent")
        self.assertEqual(
            self.registry.supervisor_for(security), "executive/chief-security-officer-agent"
        )

    def test_executives_report_to_the_ceo(self) -> None:
        cto = self.registry.get("executive/cto-agent")
        self.assertEqual(self.registry.supervisor_for(cto), self.registry.ceo_id)

    def test_ceo_is_the_root(self) -> None:
        ceo = self.registry.get(self.registry.ceo_id)
        self.assertIsNone(self.registry.supervisor_for(ceo))


class LookupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()

    def test_resolve_by_id_slug_and_human_name(self) -> None:
        expected = "security/security-architect-agent"
        for reference in (
            expected,
            "security-architect-agent",
            "Security Architect Agent",
        ):
            self.assertEqual(self.registry.resolve(reference).id, expected, reference)

    def test_unknown_reference_raises(self) -> None:
        with self.assertRaises(AgentNotFoundError):
            self.registry.resolve("Chief Vibes Officer")

    def test_with_capability_matches_namespace_prefix(self) -> None:
        exact = self.registry.with_capability("security.threat-modeling")
        namespace = self.registry.with_capability("security")
        self.assertTrue(exact)
        self.assertGreaterEqual(len(namespace), len(exact))

    def test_a_new_spec_becomes_selectable_with_no_code_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = support.synthetic_repo(Path(tmp))
            before = AgentRegistry.discover(root)
            self.assertNotIn("hardware/antenna-engineer", before)

            support.write_spec(
                root,
                "hardware",
                "antenna-engineer",
                name="Antenna Engineer Agent",
                mission="Design PCB antennas and validate their circuit performance.",
                responsibilities="- Own antenna schematic and PCB layout",
            )
            after = AgentRegistry.discover(root)
            self.assertIn("hardware/antenna-engineer", after)
            self.assertIn(
                "hardware.electrical", after.get("hardware/antenna-engineer").capabilities
            )


if __name__ == "__main__":
    unittest.main()
