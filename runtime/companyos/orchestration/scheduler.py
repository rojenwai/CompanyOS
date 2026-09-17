"""DAG scheduler.

Runs every task whose dependencies are satisfied, concurrently, up to
``max_parallel``. A task starts the moment its own dependencies finish -- the
scheduler does not wait for a whole wave to complete -- so an independent
branch is never held up by a slow sibling.

Dependent tasks are never parallelized:

    Research -> Analysis -> Recommendation

stays strictly sequential because each node's dependency must reach COMPLETED
before it becomes ready.
"""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

from ..config import RuntimeConfig
from ..errors import LimitExceeded
from ..ids import now
from ..models import AgentResult, Task, TaskGraph
from ..observability import EventBus, EventType
from ..status import TaskStatus

ExecuteFn = Callable[[Task], Awaitable[AgentResult]]


class DAGScheduler:
    """Dependency-aware concurrent execution over a :class:`TaskGraph`."""

    def __init__(self, config: RuntimeConfig, bus: EventBus, run_id: str) -> None:
        self.config = config
        self.bus = bus
        self.run_id = run_id
        self.max_concurrent_observed = 0

    async def run(
        self,
        graph: TaskGraph,
        execute: ExecuteFn,
        *,
        cancel: asyncio.Event | None = None,
        results: dict[str, AgentResult] | None = None,
        only: "set[str] | None" = None,
    ) -> dict[str, AgentResult]:
        """Execute the graph and return ``{task_id: AgentResult}``.

        ``only`` restricts execution to a subset of task ids -- used by the
        review loop to re-run just the tasks a reviewer rejected, without
        redoing the ones it accepted.
        """
        collected: dict[str, AgentResult] = results if results is not None else {}
        running: dict[asyncio.Task, Task] = {}
        deadline = now() + self.config.limits.run_timeout_s
        limit_error: LimitExceeded | None = None

        try:
            while True:
                self._skip_blocked(graph, only)

                if cancel is not None and cancel.is_set():
                    break
                if now() >= deadline:
                    self.bus.emit(
                        EventType.LIMIT_HIT,
                        run_id=self.run_id,
                        message="run timeout reached; stopping the scheduler",
                        data={"limit": "run_timeout_s"},
                    )
                    break

                if limit_error is None:
                    for task in self._launchable(graph, running, only):
                        if len(running) >= self.config.limits.max_parallel:
                            break
                        task.mark(TaskStatus.SPAWNING)
                        running[asyncio.ensure_future(self._guard(execute, task))] = task
                        self.max_concurrent_observed = max(
                            self.max_concurrent_observed, len(running)
                        )

                if not running:
                    break

                done, _ = await asyncio.wait(
                    running,
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=max(0.01, deadline - now()),
                )
                if not done:
                    continue  # loop back to re-check the deadline and cancellation

                for future in done:
                    task = running.pop(future)
                    try:
                        result = future.result()
                    except LimitExceeded as exc:
                        # A run-level budget stop: finish what is in flight, start
                        # nothing new, and report the rest as skipped.
                        limit_error = exc
                        task.mark(TaskStatus.SKIPPED, error=str(exc))
                        self.bus.emit(
                            EventType.LIMIT_HIT,
                            run_id=self.run_id,
                            task_id=task.id,
                            message=str(exc),
                            data={"limit": exc.limit},
                        )
                        continue
                    except asyncio.CancelledError:
                        task.mark(TaskStatus.CANCELLED, error="cancelled")
                        continue

                    collected[task.id] = result
                    task.output = result.output
                    task.assigned_agent = result.agent_id
                    task.mark(
                        result.status,
                        error="; ".join(result.errors) if result.errors else None,
                    )
                    self.bus.emit(
                        EventType.TASK_STATUS,
                        run_id=self.run_id,
                        task_id=task.id,
                        agent_id=result.agent_id,
                        message=result.status.value,
                        data={"duration_s": round(result.execution_time_s, 3)},
                    )
        finally:
            for future in running:
                future.cancel()
            if running:
                await asyncio.gather(*running, return_exceptions=True)
            for task in running.values():
                if not task.status.terminal:
                    task.mark(TaskStatus.CANCELLED, error="scheduler stopped")

        self._finalize(graph, cancel, only)
        return collected

    # -- internals -------------------------------------------------------------

    async def _guard(self, execute: ExecuteFn, task: Task) -> AgentResult:
        """Apply the per-task timeout."""
        try:
            return await asyncio.wait_for(
                execute(task), timeout=self.config.limits.task_timeout_s
            )
        except asyncio.TimeoutError:
            self.bus.emit(
                EventType.AGENT_TIMEOUT,
                run_id=self.run_id,
                task_id=task.id,
                agent_id=task.assigned_agent or "",
                message=f"task exceeded {self.config.limits.task_timeout_s}s",
            )
            return AgentResult(
                agent_id=task.assigned_agent or "unassigned",
                task_id=task.id,
                status=TaskStatus.FAILED,
                errors=[f"timeout after {self.config.limits.task_timeout_s}s"],
                completed_at=now(),
            )

    def _launchable(
        self, graph: TaskGraph, running: dict, only: "set[str] | None"
    ) -> list[Task]:
        in_flight = {t.id for t in running.values()}
        return [
            task
            for task in graph.ready_tasks()
            if task.id not in in_flight and (only is None or task.id in only)
        ]

    def _skip_blocked(self, graph: TaskGraph, only: "set[str] | None") -> None:
        """Mark tasks whose required dependency failed. One bad branch does not
        fail the run -- only the subtree that genuinely needed it."""
        for task in graph.blocked_tasks():
            if only is not None and task.id not in only:
                continue
            if task.status.terminal:
                continue
            failed = [
                d
                for d in task.dependencies
                if (dep := graph.get(d)) and dep.status.terminal and not dep.status.successful
            ]
            task.mark(TaskStatus.SKIPPED, error=f"dependency failed: {', '.join(failed)}")
            self.bus.emit(
                EventType.TASK_SKIPPED,
                run_id=self.run_id,
                task_id=task.id,
                message=f"skipped; dependency failed: {', '.join(failed)}",
                data={"failed_dependencies": failed},
            )

    def _finalize(self, graph: TaskGraph, cancel: asyncio.Event | None, only: "set[str] | None") -> None:
        cancelled = cancel is not None and cancel.is_set()
        for task in graph:
            if task.status.terminal:
                continue
            if only is not None and task.id not in only:
                continue
            if cancelled:
                task.mark(TaskStatus.CANCELLED, error="run cancelled")
            else:
                task.mark(TaskStatus.SKIPPED, error="not reached before the run ended")
