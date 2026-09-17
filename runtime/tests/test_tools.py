"""Tool sandboxing and permission boundaries."""

from __future__ import annotations

import unittest

from companyos.errors import ToolPermissionError
from companyos.memory import FileMemoryStore
from companyos.tools import ToolContext, ToolRegistry
from companyos.tools.policy import resolve_policy

from . import support


def context(**kwargs):
    config = support.config()
    defaults = dict(
        root=config.root,
        run_id="run_1",
        task_id="task_1",
        agent_id="engineering/backend-engineer",
        readable_dirs=config.readable_dirs,
    )
    defaults.update(kwargs)
    return ToolContext(**defaults)


class PolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()
        self.tools = ToolRegistry.default()

    def test_denied_tool_raises_on_check(self) -> None:
        policy = resolve_policy(
            self.registry.get("engineering/backend-engineer"), support.config(), self.tools
        )
        with self.assertRaises(ToolPermissionError):
            policy.check("shell")

    def test_ungranted_tool_raises_on_check(self) -> None:
        policy = resolve_policy(
            self.registry.get("engineering/backend-engineer"), support.config(), self.tools
        )
        with self.assertRaises(ToolPermissionError):
            policy.check("run_checks")

    def test_granted_tool_passes(self) -> None:
        policy = resolve_policy(
            self.registry.get("engineering/backend-engineer"), support.config(), self.tools
        )
        self.assertIsNone(policy.check("read_spec"))

    def test_spec_prohibition_is_honoured(self) -> None:
        """A spec that forbids a tool loses it even if the runtime allows it."""
        from dataclasses import replace

        definition = self.registry.get("engineering/backend-engineer")
        narrowed = replace(definition, prohibited_tools=("read_spec",))
        policy = resolve_policy(narrowed, support.config(), self.tools)
        self.assertNotIn("read_spec", policy.allowed)
        self.assertIn("read_spec", policy.denied)

    def test_unknown_tools_are_dropped(self) -> None:
        from dataclasses import replace

        definition = replace(
            self.registry.get("engineering/backend-engineer"), tools=("telepathy",)
        )
        policy = resolve_policy(definition, support.config(), self.tools)
        self.assertNotIn("telepathy", policy.allowed)


class SandboxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tools = ToolRegistry.default()
        self.context = context()

    def _read(self, path: str):
        return self.tools.get("read_spec").invoke({"path": path}, self.context)

    def test_reads_a_spec_inside_the_sandbox(self) -> None:
        result = self._read("ai/agents/engineering/backend-engineer.md")
        self.assertTrue(result.ok)
        self.assertIn("Backend Engineer", result.content)

    def test_traversal_is_blocked(self) -> None:
        result = self._read("../../../etc/passwd")
        self.assertFalse(result.ok)
        self.assertIn("escapes", result.error)

    def test_absolute_paths_are_blocked(self) -> None:
        for path in ("/etc/passwd", "C:/Windows/System32/drivers/etc/hosts"):
            with self.subTest(path=path):
                result = self._read(path)
                self.assertFalse(result.ok)
                self.assertIn("absolute", result.error)

    def test_directories_outside_the_readable_set_are_blocked(self) -> None:
        result = self._read("scripts/check-links.py")
        self.assertFalse(result.ok)
        self.assertIn("outside the readable set", result.error)

    def test_non_text_files_are_blocked(self) -> None:
        result = self._read("ai")  # a directory, not a file
        self.assertFalse(result.ok)

    def test_missing_file_reports_cleanly(self) -> None:
        result = self._read("ai/agents/engineering/nonexistent.md")
        self.assertFalse(result.ok)
        self.assertIn("no such file", result.error)

    def test_search_is_confined_to_readable_dirs(self) -> None:
        result = self.tools.get("search_specs").invoke(
            {"query": "threat model", "limit": 5}, self.context
        )
        self.assertTrue(result.ok)
        for line in result.content.splitlines():
            self.assertTrue(line.startswith(("ai/", "handbook/", "starter-kits/")), line)

    def test_short_queries_are_rejected(self) -> None:
        result = self.tools.get("search_specs").invoke({"query": "a"}, self.context)
        self.assertFalse(result.ok)


class RefusedToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tools = ToolRegistry.default()

    def test_shell_network_and_writes_refuse_even_if_reached(self) -> None:
        for name in ("shell", "write_file", "http_request", "run_checks"):
            with self.subTest(tool=name):
                result = self.tools.get(name).invoke({"anything": 1}, context())
                self.assertFalse(result.ok)
                self.assertIn("not available", result.error)


class MemoryToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tools = ToolRegistry.default()
        self.memory = FileMemoryStore(support.REPO_ROOT)
        self.context = context(memory=self.memory)

    def test_recall_returns_sourced_records(self) -> None:
        result = self.tools.get("recall_memory").invoke(
            {"query": "decision memory retention versioning", "k": 2}, self.context
        )
        self.assertTrue(result.ok)
        self.assertIn("ai/memory/", result.content)

    def test_recall_says_so_when_nothing_matches(self) -> None:
        result = self.tools.get("recall_memory").invoke(
            {"query": "zzzqqxx nonexistent term"}, self.context
        )
        self.assertEqual(result.content, "no reliable source")

    def test_remember_only_proposes(self) -> None:
        result = self.tools.get("remember").invoke(
            {"store": "session-memory", "text": "A fact.", "tags": ["test"]}, self.context
        )
        self.assertTrue(result.ok)
        self.assertIn("only after promotion", result.content)
        proposals = self.memory.proposals()
        self.assertEqual(len(proposals), 1)
        self.assertFalse(proposals[0].promoted)

    def test_untagged_memory_is_rejected(self) -> None:
        result = self.tools.get("remember").invoke(
            {"store": "session-memory", "text": "A fact.", "tags": []}, self.context
        )
        self.assertIn("rejected", result.content)


if __name__ == "__main__":
    unittest.main()
