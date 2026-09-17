"""Dynamic spawning: instance lifecycle, tool grants, and the spawn budget."""

from __future__ import annotations

import unittest

from companyos.config import Budget
from companyos.errors import LimitExceeded, ProviderError
from companyos.models import Task
from companyos.observability import EventType
from companyos.orchestration.context import ContextBuilder
from companyos.orchestration.spawner import AgentSpawner
from companyos.providers import Completion, Message, Provider, ToolCall
from companyos.status import TaskStatus
from companyos.tools import ToolRegistry

from . import support


def make_spawner(config=None, provider=None, bus=None, memory=None):
    config = config or support.config()
    bus = bus or support.bus()
    spawner = AgentSpawner(
        config,
        provider or support.provider(),
        ToolRegistry.default(),
        bus,
        Budget(config.limits),
        memory,
    )
    return spawner, bus, config


def bundle_for(task: Task, config=None):
    from companyos.models import TaskGraph

    graph = TaskGraph([task])
    return ContextBuilder(config or support.config()).build(task, graph, {})


class SpawnTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()
        self.definition = self.registry.get("engineering/backend-engineer")

    def test_spawning_creates_a_temporary_instance(self) -> None:
        spawner, bus, _ = make_spawner()
        task = Task(objective="Implement the token endpoint")
        instance = spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")

        self.assertEqual(instance.definition.id, self.definition.id)
        self.assertEqual(instance.task.id, task.id)
        self.assertIn(instance.id, spawner.live)
        self.assertTrue(bus.of_type(EventType.AGENT_SPAWNED))

    def test_each_spawn_is_a_distinct_instance(self) -> None:
        spawner, _, _ = make_spawner()
        a, b = Task(objective="one"), Task(objective="two")
        first = spawner.spawn(self.definition, a, bundle_for(a), run_id="run_1")
        second = spawner.spawn(self.definition, b, bundle_for(b), run_id="run_1")
        self.assertNotEqual(first.id, second.id)
        self.assertIs(first.definition, second.definition, "the definition is shared")

    def test_instance_executes_and_returns_a_structured_result(self) -> None:
        spawner, _, _ = make_spawner()
        task = Task(objective="Implement the token endpoint",
                    acceptance_criteria=["endpoint returns a signed token"])
        instance = spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")
        result = support.run(instance.run())

        self.assertTrue(result.ok)
        self.assertEqual(result.status, TaskStatus.COMPLETED)
        self.assertEqual(result.agent_id, "engineering/backend-engineer")
        self.assertEqual(result.task_id, task.id)
        self.assertTrue(result.output)
        self.assertGreater(result.usage.total, 0)
        self.assertGreater(result.execution_time_s, 0)
        self.assertEqual(result.provider, "mock")

    def test_instances_are_terminated_when_retired(self) -> None:
        spawner, bus, _ = make_spawner()
        task = Task(objective="one")
        instance = spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")
        spawner.retire(instance)
        self.assertNotIn(instance.id, spawner.live)
        self.assertTrue(bus.of_type(EventType.AGENT_TERMINATED))

    def test_provider_failure_becomes_a_failed_result_not_an_exception(self) -> None:
        provider = support.provider(fail_agents=["engineering/backend-engineer"])
        spawner, _, _ = make_spawner(provider=provider)
        task = Task(objective="Implement the token endpoint")
        instance = spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")
        result = support.run(instance.run())

        self.assertFalse(result.ok)
        self.assertEqual(result.status, TaskStatus.FAILED)
        self.assertTrue(result.errors)


class LimitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.definition = support.repo_registry().get("engineering/backend-engineer")

    def test_max_agents_stops_runaway_spawning(self) -> None:
        config = support.config(limits={"max_agents": 3})
        spawner, bus, _ = make_spawner(config=config)
        for index in range(3):
            task = Task(objective=f"task {index}")
            spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")

        overflow = Task(objective="one too many")
        with self.assertRaises(LimitExceeded) as caught:
            spawner.spawn(self.definition, overflow, bundle_for(overflow), run_id="run_1")
        self.assertEqual(caught.exception.limit, "max_agents")
        self.assertEqual(len(spawner.spawned), 3)

    def test_max_depth_stops_unbounded_nesting(self) -> None:
        config = support.config(limits={"max_depth": 2})
        spawner, _, _ = make_spawner(config=config)
        deep = Task(objective="too deep", depth=3)
        with self.assertRaises(LimitExceeded) as caught:
            spawner.spawn(self.definition, deep, bundle_for(deep), run_id="run_1")
        self.assertEqual(caught.exception.limit, "max_depth")

    def test_tool_call_budget_is_bounded(self) -> None:
        """An agent that only ever asks for tools is cut off, not looped forever."""

        class AlwaysToolProvider(Provider):
            name = "always-tools"
            default_model = "loop-1"

            def __init__(self) -> None:
                super().__init__(support.config().provider)
                self.calls = 0

            async def complete(self, **kwargs) -> Completion:
                self.calls += 1
                return Completion(
                    text="",
                    tool_calls=(ToolCall("c", "read_spec", {"path": "ai/README.md"}),),
                    provider=self.name,
                    model=self.model,
                )

        config = support.config(limits={"max_tool_calls_per_agent": 3})
        provider = AlwaysToolProvider()
        spawner, _, _ = make_spawner(config=config, provider=provider)
        task = Task(objective="loop forever")
        instance = spawner.spawn(self.definition, task, bundle_for(task), run_id="run_1")
        result = support.run(instance.run())

        self.assertEqual(provider.calls, 4, "max_tool_calls + the final attempt")
        self.assertTrue(any("budget" in e for e in result.errors))


class ToolGrantTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = support.repo_registry()

    def test_read_only_floor_is_granted(self) -> None:
        spawner, _, _ = make_spawner()
        definition = self.registry.get("engineering/backend-engineer")
        task = Task(objective="one")
        instance = spawner.spawn(definition, task, bundle_for(task), run_id="run_1")
        self.assertIn("read_spec", instance.policy.allowed)
        self.assertIn("recall_memory", instance.policy.allowed)

    def test_runtime_denylist_overrides_the_spec(self) -> None:
        spawner, _, _ = make_spawner()
        definition = self.registry.get("engineering/backend-engineer")
        task = Task(objective="one")
        instance = spawner.spawn(definition, task, bundle_for(task), run_id="run_1")
        for forbidden in ("shell", "write_file", "http_request"):
            self.assertNotIn(forbidden, instance.policy.allowed, forbidden)

    def test_mutating_tools_are_not_granted_implicitly(self) -> None:
        """The Backend Engineer spec names code execution; the runtime does not
        grant it, because run_checks is mutating and not on the operator's list."""
        definition = self.registry.get("engineering/backend-engineer")
        self.assertIn("run_checks", definition.tools)
        spawner, _, _ = make_spawner()
        task = Task(objective="one")
        instance = spawner.spawn(definition, task, bundle_for(task), run_id="run_1")
        self.assertNotIn("run_checks", instance.policy.allowed)
        self.assertIn("run_checks", instance.policy.denied)

    def test_operator_can_grant_a_mutating_tool_explicitly(self) -> None:
        config = support.config(
            default_tools=("read_spec", "recall_memory", "remember")
        )
        spawner, _, _ = make_spawner(config=config)
        definition = self.registry.get("engineering/backend-engineer")
        task = Task(objective="one")
        instance = spawner.spawn(definition, task, bundle_for(task), run_id="run_1")
        self.assertIn("remember", instance.policy.allowed)

    def test_only_granted_tools_are_offered_to_the_model(self) -> None:
        provider = support.provider()
        spawner, _, _ = make_spawner(provider=provider)
        definition = self.registry.get("engineering/backend-engineer")
        task = Task(objective="one")
        instance = spawner.spawn(definition, task, bundle_for(task), run_id="run_1")
        support.run(instance.run())

        offered = set(provider.calls[-1].tools)
        self.assertEqual(offered, set(instance.policy.allowed))
        self.assertNotIn("shell", offered)


if __name__ == "__main__":
    unittest.main()
