"""Result aggregation.

Collects what the parallel branches produced -- successes, failures, and the
partial picture in between -- and renders it for the reviewer and the
synthesizer. A run that lost one non-critical branch still aggregates; the
aggregation says plainly what is missing rather than hiding the gap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from ..models import AgentResult, Task, TaskGraph, Usage
from ..status import TaskStatus
from .prompts import untrusted

_MAX_OUTPUT_CHARS = 6_000


@dataclass
class Aggregation:
    """The collected state of one execution pass."""

    successes: list[tuple[Task, AgentResult]] = field(default_factory=list)
    failures: list[tuple[Task, AgentResult | None]] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)

    @property
    def complete(self) -> bool:
        """True when nothing failed or was skipped."""
        return not self.failures and not self.skipped

    @property
    def partial(self) -> bool:
        return bool(self.successes) and not self.complete

    @property
    def empty(self) -> bool:
        return not self.successes

    @property
    def task_ids(self) -> list[str]:
        return [task.id for task, _ in self.successes]

    def metadata(self) -> dict:
        durations = [r.execution_time_s for _, r in self.successes]
        return {
            "tasks_total": len(self.successes) + len(self.failures) + len(self.skipped),
            "succeeded": len(self.successes),
            "failed": len(self.failures),
            "skipped": len(self.skipped),
            "complete": self.complete,
            "partial": self.partial,
            "agents": sorted({r.agent_id for _, r in self.successes}),
            "usage": self.usage.to_dict(),
            "slowest_s": round(max(durations), 3) if durations else 0.0,
            "total_agent_time_s": round(sum(durations), 3),
        }

    # -- rendering -------------------------------------------------------------

    def render(self, *, include_failures: bool = True) -> str:
        """A readable digest of every branch, for a reviewer or synthesizer.

        Agent output is wrapped as untrusted data: the reviewer must judge it,
        not obey it.
        """
        blocks: list[str] = []
        for task, result in self.successes:
            blocks.append(
                f"### Task {task.id} - {task.objective}\n"
                f"Agent: {result.agent_name or result.agent_id} ({result.agent_id})\n"
                f"Acceptance criteria: "
                f"{'; '.join(task.acceptance_criteria) or 'none stated'}\n\n"
                + untrusted(f"agent:{result.agent_id}", result.output[:_MAX_OUTPUT_CHARS])
            )
        if include_failures:
            for task, result in self.failures:
                errors = "; ".join(result.errors) if result else task.error or "unknown error"
                blocks.append(f"### Task {task.id} - {task.objective}\nFAILED: {errors}")
            for task in self.skipped:
                blocks.append(
                    f"### Task {task.id} - {task.objective}\nSKIPPED: {task.error or 'not run'}"
                )
        return "\n\n".join(blocks) if blocks else "No results were produced."

    def summaries(self) -> list[dict]:
        """Compact per-task records, used by the synthesizer's context."""
        return [
            {
                "task_id": task.id,
                "objective": task.objective,
                "agent": result.agent_name or result.agent_id,
                "agent_id": result.agent_id,
                "status": result.status.value,
                "duration_s": round(result.execution_time_s, 3),
            }
            for task, result in self.successes
        ]

    def gaps(self) -> list[str]:
        """Plain statements of what is missing, for the final response."""
        out = [f"{t.objective}: failed ({(r.errors[0] if r and r.errors else t.error)})"
               for t, r in self.failures]
        out += [f"{t.objective}: not run ({t.error})" for t in self.skipped]
        return out


class ResultAggregator:
    """Turns a graph plus its results into an :class:`Aggregation`."""

    def collect(
        self, graph: TaskGraph, results: Mapping[str, AgentResult]
    ) -> Aggregation:
        aggregation = Aggregation()
        for task in graph.topological_order():
            result = results.get(task.id)
            if result is not None and result.ok:
                aggregation.successes.append((task, result))
                aggregation.usage = aggregation.usage + result.usage
            elif task.status is TaskStatus.SKIPPED:
                aggregation.skipped.append(task)
            elif result is not None or task.status.terminal:
                aggregation.failures.append((task, result))
                if result is not None:
                    aggregation.usage = aggregation.usage + result.usage
        return aggregation
