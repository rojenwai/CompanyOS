"""The Agent Map: the execution graph a UI would render."""

from __future__ import annotations

import json
import unittest

from companyos import purposes
from companyos.orchestration import Orchestrator, build_agent_map, render_tree

from . import support


class AgentMapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orchestrator = Orchestrator(
            support.config(),
            registry=support.repo_registry(),
            provider=support.provider(),
            bus=support.bus(),
            trace_to_disk=False,
        )
        cls.record = cls.orchestrator.run_sync(
            "Design and implement authentication for a web application."
        )
        cls.map = cls.orchestrator.agent_map(cls.record)

    def nodes_of_kind(self, kind: str) -> list[dict]:
        return [n for n in self.map["nodes"] if n["kind"] == kind]

    def test_document_shape(self) -> None:
        for key in ("run_id", "root_task", "nodes", "edges", "status", "counts"):
            self.assertIn(key, self.map, key)
        self.assertEqual(self.map["run_id"], self.record.id)
        self.assertEqual(self.map["root_task"], self.record.request)

    def test_every_node_has_the_documented_fields(self) -> None:
        for node in self.map["nodes"]:
            for key in ("id", "parent_id", "agent", "task", "status"):
                self.assertIn(key, node, f"{node['id']} missing {key}")

    def test_there_is_exactly_one_root(self) -> None:
        roots = [n for n in self.map["nodes"] if n["parent_id"] is None]
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0]["kind"], "entry")

    def test_every_parent_reference_resolves(self) -> None:
        ids = {n["id"] for n in self.map["nodes"]}
        for node in self.map["nodes"]:
            if node["parent_id"] is not None:
                self.assertIn(node["parent_id"], ids, node["id"])

    def test_every_edge_endpoint_resolves(self) -> None:
        ids = {n["id"] for n in self.map["nodes"]}
        for edge in self.map["edges"]:
            self.assertIn(edge["from"], ids)
            self.assertIn(edge["to"], ids)
            self.assertIn(edge["type"], {"delegates", "depends_on", "reviewed_by", "reports_to"})

    def test_hierarchy_runs_ceo_to_executive_to_specialist(self) -> None:
        supervisors = self.nodes_of_kind("supervisor")
        self.assertTrue(supervisors, "specialists should hang off an accountable owner")
        agents = self.nodes_of_kind("agent")
        parents = {n["parent_id"] for n in agents}
        self.assertTrue(parents & {s["id"] for s in supervisors})

    def test_supervisor_nodes_are_not_spawned_instances(self) -> None:
        for node in self.nodes_of_kind("supervisor"):
            self.assertFalse(node["spawned"])
            self.assertEqual(node["status"], "delegated")

    def test_spawned_agents_carry_execution_metadata(self) -> None:
        for node in self.nodes_of_kind("agent"):
            if not node["spawned"]:
                continue
            self.assertIsNotNone(node["instance_id"])
            self.assertIsNotNone(node["duration_s"])
            self.assertEqual(node["provider"], "mock")
            self.assertIn("total_tokens", node["usage"])
            self.assertTrue(node["required_capabilities"])
            self.assertTrue(node["context_keys"])

    def test_statuses_carry_the_documented_lifecycle_name(self) -> None:
        for node in self.nodes_of_kind("agent"):
            self.assertIn("spec_state", node)
            self.assertEqual(node["spec_state"], "DONE")

    def test_review_and_synthesis_are_present(self) -> None:
        self.assertTrue(self.nodes_of_kind("reviewer"))
        self.assertTrue(self.nodes_of_kind("synthesis"))

    def test_counts_summarize_the_run(self) -> None:
        counts = self.map["counts"]
        self.assertEqual(counts["nodes"], len(self.map["nodes"]))
        self.assertGreaterEqual(counts["spawned"], 3)
        self.assertEqual(counts["failed"], 0)
        self.assertEqual(counts["currently_running"], [])

    def test_map_is_json_serializable(self) -> None:
        self.assertEqual(json.loads(json.dumps(self.map))["run_id"], self.record.id)

    def test_map_is_a_pure_projection(self) -> None:
        """Rebuilding from the same run record gives the same document."""
        again = build_agent_map(self.record, self.orchestrator.registry)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.map, sort_keys=True))

    def test_tree_renders_for_a_terminal(self) -> None:
        tree = render_tree(self.map)
        self.assertIn("CEO Agent", tree)
        self.assertIn("Backend Engineer Agent", tree)
        self.assertLessEqual(max(len(line) for line in tree.splitlines()), 120)


class DependencyEdgeTest(unittest.TestCase):
    def test_sequential_plans_produce_dependency_edges(self) -> None:
        provider = support.provider(
            script={
                purposes.DECOMPOSE: json.dumps(
                    {"tasks": [
                        {"id": "r", "objective": "Size the market",
                         "required_capabilities": ["research.market"]},
                        {"id": "s", "objective": "Recommend a pricing strategy",
                         "required_capabilities": ["strategy.pricing"], "dependencies": ["r"]},
                    ]}
                )
            }
        )
        orchestrator = Orchestrator(
            support.config(),
            registry=support.repo_registry(),
            provider=provider,
            bus=support.bus(),
            trace_to_disk=False,
        )
        run = orchestrator.run_sync("Should we build and price this?")
        agent_map = orchestrator.agent_map(run)

        depends = [e for e in agent_map["edges"] if e["type"] == "depends_on"]
        self.assertEqual(len(depends), 1)

    def test_failed_nodes_are_visible_with_their_errors(self) -> None:
        provider = support.provider(fail_agents=["research/market-research-agent"])
        orchestrator = Orchestrator(
            support.config(),
            registry=support.repo_registry(),
            provider=provider,
            bus=support.bus(),
            trace_to_disk=False,
        )
        run = orchestrator.run_sync(
            "Research whether a developer-tools product idea has a viable market."
        )
        agent_map = orchestrator.agent_map(run)

        failed = [n for n in agent_map["nodes"] if n["status"] == "failed"]
        self.assertTrue(failed)
        self.assertTrue(failed[0]["errors"])
        self.assertEqual(agent_map["counts"]["failed"], len(failed))


if __name__ == "__main__":
    unittest.main()
