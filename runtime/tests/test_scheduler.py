"""Concurrent DAG execution: parallelism, sequencing, timeouts, cancellation."""

from __future__ import annotations

import asyncio
import time
import unittest

from companyos.ids import now
from companyos.models import AgentResult, Task, TaskGraph
from companyos.orchestration.scheduler import DAGScheduler
from companyos.status import TaskStatus

from . import support


class Recorder:
    """An execute function that tracks overlap and ordering."""

    def __init__(self, delay: float = 0.05, fail: tuple[str, ...] = ()) -> None:
        self.delay = delay
        self.fail = set(fail)
        self.order: list[str] = []
        self.finished: list[str] = []
        self.live = 0
        self.peak = 0

    async def __call__(self, task: Task) -> AgentResult:
        self.order.append(task.objective)
        self.live += 1
        self.peak = max(self.peak, self.live)
        try:
            await asyncio.sleep(self.delay)
        finally:
            self.live -= 1
        self.finished.append(task.objective)

        failed = task.objective in self.fail
        return AgentResult(
            agent_id=f"test/{task.objective}",
            task_id=task.id,
            status=TaskStatus.FAILED if failed else TaskStatus.COMPLETED,
            output="" if failed else f"output of {task.objective}",
            errors=["simulated failure"] if failed else [],
            completed_at=now(),
        )


def schedule(graph: TaskGraph, recorder: Recorder, **limits):
    config = support.config(limits=limits)
    scheduler = DAGScheduler(config, support.bus(), "run_test")
    results = support.run(scheduler.run(graph, recorder))
    return results, scheduler


class ParallelExecutionTest(unittest.TestCase):
    def test_independent_tasks_run_concurrently(self) -> None:
        graph = support.parallel_graph("a", "b", "c")
        recorder = Recorder(delay=0.08)

        started = time.perf_counter()
        results, scheduler = schedule(graph, recorder, max_parallel=3)
        elapsed = time.perf_counter() - started

        self.assertEqual(len(results), 3)
        self.assertEqual(recorder.peak, 3, "all three should overlap")
        self.assertEqual(scheduler.max_concurrent_observed, 3)
        self.assertLess(elapsed, 0.24, "concurrent execution should beat 3 x 0.08s")

    def test_concurrency_is_capped(self) -> None:
        graph = support.parallel_graph("a", "b", "c", "d", "e")
        recorder = Recorder(delay=0.03)
        schedule(graph, recorder, max_parallel=2)
        self.assertLessEqual(recorder.peak, 2)

    def test_a_slow_branch_does_not_hold_up_an_independent_one(self) -> None:
        """A task starts when its own dependencies finish, not when a wave does."""
        graph = TaskGraph()
        slow = graph.add(Task(objective="slow"))
        quick = graph.add(Task(objective="quick"))
        graph.add(support.task("after-quick", deps=(quick.id,)))
        graph.validate()

        class Variable(Recorder):
            async def __call__(self, task: Task) -> AgentResult:
                self.delay = 0.20 if task.objective == "slow" else 0.01
                return await super().__call__(task)

        recorder = Variable()
        schedule(graph, recorder, max_parallel=3)
        # after-quick finishes before slow, proving it did not wait for the wave.
        self.assertLess(
            recorder.finished.index("after-quick"), recorder.finished.index("slow")
        )


class SequentialExecutionTest(unittest.TestCase):
    def test_dependent_tasks_never_overlap(self) -> None:
        graph = support.linear_graph("research", "analysis", "recommendation")
        recorder = Recorder(delay=0.02)
        results, _ = schedule(graph, recorder, max_parallel=4)

        self.assertEqual(len(results), 3)
        self.assertEqual(recorder.peak, 1, "a dependency chain must not parallelize")
        self.assertEqual(recorder.order, ["research", "analysis", "recommendation"])

    def test_diamond_runs_the_middle_in_parallel(self) -> None:
        graph = TaskGraph()
        research = graph.add(Task(objective="research"))
        competitor = graph.add(support.task("competitor", deps=(research.id,)))
        market = graph.add(support.task("market", deps=(research.id,)))
        graph.add(support.task("strategy", deps=(competitor.id, market.id)))
        graph.validate()

        recorder = Recorder(delay=0.04)
        schedule(graph, recorder, max_parallel=4)
        self.assertEqual(recorder.peak, 2, "only the middle pair is independent")
        self.assertEqual(recorder.order[0], "research")
        self.assertEqual(recorder.order[-1], "strategy")


class FailureHandlingTest(unittest.TestCase):
    def test_a_failed_dependency_skips_only_its_subtree(self) -> None:
        graph = TaskGraph()
        good = graph.add(Task(objective="good"))
        bad = graph.add(Task(objective="bad"))
        downstream = graph.add(support.task("downstream", deps=(bad.id,)))
        graph.validate()

        recorder = Recorder(delay=0.01, fail=("bad",))
        results, _ = schedule(graph, recorder, max_parallel=3)

        self.assertEqual(graph[good.id].status, TaskStatus.COMPLETED)
        self.assertEqual(graph[bad.id].status, TaskStatus.FAILED)
        self.assertEqual(graph[downstream.id].status, TaskStatus.SKIPPED)
        self.assertNotIn("downstream", recorder.order, "skipped work must not execute")
        self.assertIn(good.id, results)

    def test_one_failure_does_not_end_the_run(self) -> None:
        graph = support.parallel_graph("a", "bad", "c")
        recorder = Recorder(delay=0.01, fail=("bad",))
        results, _ = schedule(graph, recorder, max_parallel=3)
        succeeded = [r for r in results.values() if r.ok]
        self.assertEqual(len(succeeded), 2)

    def test_optional_failure_lets_dependents_proceed(self) -> None:
        graph = TaskGraph()
        optional = graph.add(Task(objective="optional-input", optional=True))
        graph.add(support.task("consumer", deps=(optional.id,)))
        graph.validate()

        recorder = Recorder(delay=0.01, fail=("optional-input",))
        schedule(graph, recorder, max_parallel=2)
        self.assertIn("consumer", recorder.order)

    def test_task_timeout_fails_only_that_task(self) -> None:
        graph = support.parallel_graph("quick", "hangs")

        async def execute(task: Task) -> AgentResult:
            await asyncio.sleep(1.0 if task.objective == "hangs" else 0.01)
            return AgentResult(
                agent_id="test", task_id=task.id, status=TaskStatus.COMPLETED,
                output="ok", completed_at=now(),
            )

        config = support.config(limits={"task_timeout_s": 0.1, "max_parallel": 2})
        scheduler = DAGScheduler(config, support.bus(), "run_test")
        results = support.run(scheduler.run(graph, execute))

        statuses = {t.objective: t.status for t in graph}
        self.assertEqual(statuses["quick"], TaskStatus.COMPLETED)
        self.assertEqual(statuses["hangs"], TaskStatus.FAILED)
        self.assertIn("timeout", " ".join(results[graph.tasks[1].id].errors).lower())


class CancellationTest(unittest.TestCase):
    def test_cancellation_stops_new_work(self) -> None:
        graph = support.parallel_graph("a", "b", "c", "d")
        cancel = asyncio.Event()
        started: list[str] = []

        async def execute(task: Task) -> AgentResult:
            started.append(task.objective)
            cancel.set()
            await asyncio.sleep(0.01)
            return AgentResult(
                agent_id="test", task_id=task.id, status=TaskStatus.COMPLETED,
                output="ok", completed_at=now(),
            )

        async def main():
            config = support.config(limits={"max_parallel": 1})
            scheduler = DAGScheduler(config, support.bus(), "run_test")
            return await scheduler.run(graph, execute, cancel=cancel)

        support.run(main())
        self.assertLess(len(started), 4)
        self.assertTrue(
            any(t.status is TaskStatus.CANCELLED for t in graph),
            "unstarted work should be marked cancelled",
        )

    def test_run_timeout_stops_the_scheduler(self) -> None:
        graph = support.parallel_graph("a", "b", "c")

        async def execute(task: Task) -> AgentResult:
            await asyncio.sleep(0.3)
            return AgentResult(
                agent_id="test", task_id=task.id, status=TaskStatus.COMPLETED,
                output="ok", completed_at=now(),
            )

        config = support.config(limits={"run_timeout_s": 0.1, "max_parallel": 1,
                                        "task_timeout_s": 5.0})
        scheduler = DAGScheduler(config, support.bus(), "run_test")
        results = support.run(scheduler.run(graph, execute))
        self.assertLess(len(results), 3)


if __name__ == "__main__":
    unittest.main()
