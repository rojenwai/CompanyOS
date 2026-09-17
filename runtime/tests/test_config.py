"""Configuration, root discovery, and the budget counters."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from companyos.config import Budget, RuntimeConfig, RuntimeLimits, find_repo_root
from companyos.errors import ConfigError, LimitExceeded

from . import support


class RootDiscoveryTest(unittest.TestCase):
    def test_finds_the_repo_root_from_a_subdirectory(self) -> None:
        found = find_repo_root(support.REPO_ROOT / "ai" / "agents" / "engineering")
        self.assertEqual(found, support.REPO_ROOT)

    def test_env_var_overrides_the_search(self) -> None:
        previous = os.environ.get("COMPANYOS_ROOT")
        os.environ["COMPANYOS_ROOT"] = str(support.REPO_ROOT)
        try:
            self.assertEqual(find_repo_root(Path(tempfile.gettempdir())), support.REPO_ROOT)
        finally:
            os.environ.pop("COMPANYOS_ROOT", None)
            if previous is not None:
                os.environ["COMPANYOS_ROOT"] = previous

    def test_a_directory_without_specs_is_rejected(self) -> None:
        previous = os.environ.pop("COMPANYOS_ROOT", None)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ConfigError):
                    find_repo_root(Path(tmp))
        finally:
            if previous is not None:
                os.environ["COMPANYOS_ROOT"] = previous


class LimitsTest(unittest.TestCase):
    def test_defaults_are_bounded(self) -> None:
        limits = RuntimeLimits()
        limits.validate()
        self.assertGreater(limits.max_agents, 0)
        self.assertGreater(limits.run_timeout_s, limits.task_timeout_s - 1)

    def test_nonsense_limits_are_rejected(self) -> None:
        for kwargs in ({"max_agents": 0}, {"max_depth": -1}, {"task_timeout_s": 0}):
            with self.subTest(**kwargs):
                with self.assertRaises(ConfigError):
                    RuntimeLimits(**kwargs).validate()

    def test_config_validates_limits_on_construction(self) -> None:
        with self.assertRaises(ConfigError):
            RuntimeConfig(root=support.REPO_ROOT, limits=RuntimeLimits(max_parallel=0))


class BudgetTest(unittest.TestCase):
    def test_agent_budget_is_enforced(self) -> None:
        budget = Budget(RuntimeLimits(max_agents=2))
        budget.charge_agent()
        budget.charge_agent()
        self.assertEqual(budget.agents_remaining(), 0)
        with self.assertRaises(LimitExceeded):
            budget.charge_agent()

    def test_token_budget_is_enforced(self) -> None:
        budget = Budget(RuntimeLimits(max_total_tokens=100))
        budget.charge_tokens(60)
        with self.assertRaises(LimitExceeded) as caught:
            budget.charge_tokens(60)
        self.assertEqual(caught.exception.limit, "max_total_tokens")

    def test_iteration_budget_is_enforced(self) -> None:
        budget = Budget(RuntimeLimits(max_iterations=1))
        budget.charge_iteration()
        with self.assertRaises(LimitExceeded):
            budget.charge_iteration()

    def test_snapshot_reports_spend_and_caps(self) -> None:
        budget = Budget(RuntimeLimits(max_agents=4))
        budget.charge_agent()
        budget.charge_tokens(10)
        snapshot = budget.snapshot()
        self.assertEqual(snapshot["agents_spawned"], 1)
        self.assertEqual(snapshot["tokens_used"], 10)
        self.assertEqual(snapshot["limits"]["max_agents"], 4)


class ConfigFileTest(unittest.TestCase):
    def test_json_file_overrides_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "companyos.json"
            path.write_text(
                json.dumps(
                    {
                        "provider": {"name": "openai", "model": "gpt-4o-mini"},
                        "limits": {"max_agents": 3, "max_parallel": 2},
                        "denied_tools": ["shell", "write_file", "http_request", "remember"],
                    }
                ),
                encoding="utf-8",
            )
            config = RuntimeConfig.load(root=support.REPO_ROOT, config_file=path)

            self.assertEqual(config.provider.name, "openai")
            self.assertEqual(config.limits.max_agents, 3)
            self.assertIn("remember", config.denied_tools)

    def test_invalid_json_is_reported_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "companyos.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(ConfigError):
                RuntimeConfig.load(root=support.REPO_ROOT, config_file=path)

    def test_defaults_are_read_only(self) -> None:
        config = RuntimeConfig(root=support.REPO_ROOT)
        for tool in ("shell", "write_file", "http_request"):
            self.assertIn(tool, config.denied_tools)
        self.assertFalse(config.allow_memory_promotion)


if __name__ == "__main__":
    unittest.main()
