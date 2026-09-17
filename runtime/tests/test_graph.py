"""The task DAG: dependency resolution, ordering, readiness."""

from __future__ import annotations

import unittest

from companyos.errors import CyclicDependencyError, MalformedTaskError
from companyos.models import Task, TaskGraph
from companyos.status import TaskStatus, spec_state

from . import support


class GraphConstructionTest(unittest.TestCase):
    def test_duplicate_ids_are_rejected(self) -> None:
        graph = TaskGraph()
        first = graph.add(Task(objective="a"))
        with self.assertRaises(MalformedTaskError):
            graph.add(Task(objective="b", id=first.id))

    def test_unknown_dependency_is_rejected(self) -> None:
        graph = TaskGraph([support.task("a", deps=("nope",))])
        with self.assertRaises(MalformedTaskError):
            graph.validate()

    def test_empty_objective_is_rejected(self) -> None:
        with self.assertRaises(MalformedTaskError):
            TaskGraph([Task(objective="   ")])

    def test_self_dependency_is_rejected(self) -> None:
        task = Task(objective="a")
        task.dependencies.append(task.id)
        with self.assertRaises(MalformedTaskError):
            TaskGraph([task])

    def test_cycle_is_detected(self) -> None:
        a, b = Task(objective="a"), Task(objective="b")
        a.dependencies.append(b.id)
        b.dependencies.append(a.id)
        with self.assertRaises(CyclicDependencyError):
            TaskGraph([a, b]).validate()


class OrderingTest(unittest.TestCase):
    def test_topological_order_respects_dependencies(self) -> None:
        graph = support.linear_graph("research", "analysis", "recommendation")
        order = [t.objective for t in graph.topological_order()]
        self.assertEqual(order, ["research", "analysis", "recommendation"])

    def test_layers_expose_parallel_waves(self) -> None:
        # research -> {competitor, market} -> strategy
        graph = TaskGraph()
        research = graph.add(Task(objective="research"))
        competitor = graph.add(support.task("competitor", deps=(research.id,)))
        market = graph.add(support.task("market", deps=(research.id,)))
        graph.add(support.task("strategy", deps=(competitor.id, market.id)))
        graph.validate()

        layers = [[t.objective for t in layer] for t in [None] for layer in graph.layers()]
        self.assertEqual(layers[0], ["research"])
        self.assertEqual(sorted(layers[1]), ["competitor", "market"])
        self.assertEqual(layers[2], ["strategy"])

    def test_independent_tasks_form_one_wave(self) -> None:
        graph = support.parallel_graph("a", "b", "c")
        self.assertEqual(len(graph.layers()), 1)
        self.assertEqual(len(graph.layers()[0]), 3)


class ReadinessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = support.linear_graph("research", "analysis", "recommendation")
        self.research, self.analysis, self.recommendation = self.graph.topological_order()

    def test_only_the_root_is_ready_initially(self) -> None:
        self.assertEqual([t.id for t in self.graph.ready_tasks()], [self.research.id])

    def test_dependents_unblock_on_completion(self) -> None:
        self.research.mark(TaskStatus.COMPLETED)
        self.assertEqual([t.id for t in self.graph.ready_tasks()], [self.analysis.id])

    def test_a_failed_dependency_blocks_the_subtree(self) -> None:
        self.research.mark(TaskStatus.FAILED, error="boom")
        self.assertEqual(self.graph.ready_tasks(), [])
        self.assertIn(self.analysis, self.graph.blocked_tasks())

    def test_an_optional_dependency_does_not_block(self) -> None:
        self.research.optional = True
        self.research.mark(TaskStatus.FAILED, error="boom")
        self.assertEqual([t.id for t in self.graph.ready_tasks()], [self.analysis.id])
        self.assertNotIn(self.analysis, self.graph.blocked_tasks())

    def test_ready_tasks_are_priority_ordered(self) -> None:
        graph = TaskGraph(
            [
                Task(objective="low", priority=9),
                Task(objective="high", priority=1),
                Task(objective="mid", priority=5),
            ]
        )
        self.assertEqual([t.objective for t in graph.ready_tasks()], ["high", "mid", "low"])


class StatusTest(unittest.TestCase):
    def test_runtime_status_maps_onto_the_documented_lifecycle(self) -> None:
        self.assertEqual(spec_state(TaskStatus.RUNNING), "IN_PROGRESS")
        self.assertEqual(spec_state(TaskStatus.REVIEWING), "IN_REVIEW")
        self.assertEqual(spec_state(TaskStatus.COMPLETED), "DONE")
        self.assertEqual(spec_state(TaskStatus.PENDING), "QUEUED")

    def test_terminal_statuses(self) -> None:
        self.assertTrue(TaskStatus.COMPLETED.terminal)
        self.assertTrue(TaskStatus.SKIPPED.terminal)
        self.assertFalse(TaskStatus.RUNNING.terminal)

    def test_timestamps_are_recorded(self) -> None:
        task = Task(objective="a")
        task.mark(TaskStatus.RUNNING)
        self.assertIsNotNone(task.started_at)
        task.mark(TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
        self.assertIsNotNone(task.duration_s)


if __name__ == "__main__":
    unittest.main()
