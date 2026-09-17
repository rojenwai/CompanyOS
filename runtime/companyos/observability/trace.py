"""Run tracing: every state change in a multi-agent run becomes an event.

One event stream serves three consumers: the CLI's live output, the JSONL
trace file that makes a finished run debuggable, and the Agent Map, which is
just a projection of the same state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

from ..ids import iso, now


class EventType:
    """The vocabulary of the trace stream."""

    RUN_STARTED = "run.started"
    RUN_STATUS = "run.status"
    RUN_COMPLETED = "run.completed"
    RUN_FAILED = "run.failed"
    RUN_CANCELLED = "run.cancelled"

    PLAN_CREATED = "plan.created"
    TASKS_DECOMPOSED = "tasks.decomposed"
    AGENT_SELECTED = "agent.selected"
    SELECTION_FAILED = "agent.selection_failed"

    AGENT_SPAWNED = "agent.spawned"
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    AGENT_TIMEOUT = "agent.timeout"
    AGENT_TERMINATED = "agent.terminated"

    TASK_STATUS = "task.status"
    TASK_SKIPPED = "task.skipped"
    TASK_RETRY = "task.retry"

    TOOL_CALLED = "tool.called"
    TOOL_DENIED = "tool.denied"

    MEMORY_PROPOSED = "memory.proposed"

    REVIEW_STARTED = "review.started"
    REVIEW_COMPLETED = "review.completed"
    APPROVAL_REQUIRED = "approval.required"

    SYNTHESIS_STARTED = "synthesis.started"
    LIMIT_HIT = "limit.exceeded"


@dataclass(frozen=True)
class Event:
    """A single observation. Immutable, serializable, ordered by ``ts``."""

    type: str
    run_id: str = ""
    task_id: str = ""
    agent_id: str = ""
    parent_agent_id: str = ""
    message: str = ""
    data: dict = field(default_factory=dict)
    ts: float = field(default_factory=now)

    def to_dict(self) -> dict:
        return {
            "ts": iso(self.ts),
            "type": self.type,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "parent_agent_id": self.parent_agent_id,
            "message": self.message,
            "data": self.data,
        }


Listener = Callable[[Event], None]


class EventBus:
    """Synchronous fan-out. Listener failures never fail the run."""

    def __init__(self, listeners: Iterable[Listener] = ()) -> None:
        self._listeners: list[Listener] = list(listeners)
        self.events: list[Event] = []

    def subscribe(self, listener: Listener) -> None:
        self._listeners.append(listener)

    def emit(self, type: str, **kwargs: Any) -> Event:
        event = Event(type=type, **kwargs)
        self.events.append(event)
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:  # pragma: no cover - observability must not break runs
                pass
        return event

    def of_type(self, *types: str) -> list[Event]:
        wanted = set(types)
        return [e for e in self.events if e.type in wanted]

    def to_list(self) -> list[dict]:
        return [e.to_dict() for e in self.events]


class JsonlSink:
    """Append every event to ``<dir>/<run_id>.jsonl``."""

    def __init__(self, directory: Path | str, run_id: str) -> None:
        self.path = Path(directory) / f"{run_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def __call__(self, event: Event) -> None:
        self._fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()


class ConsoleSink:
    """Human-readable progress for the CLI."""

    _ICONS = {
        EventType.AGENT_SPAWNED: "+",
        EventType.AGENT_STARTED: ">",
        EventType.AGENT_COMPLETED: "v",
        EventType.AGENT_FAILED: "x",
        EventType.AGENT_TIMEOUT: "t",
        EventType.TASK_SKIPPED: "-",
        EventType.TASK_RETRY: "~",
        EventType.REVIEW_COMPLETED: "?",
        EventType.TOOL_DENIED: "!",
        EventType.LIMIT_HIT: "!",
    }

    def __init__(self, verbose: bool = False, stream: Any = None) -> None:
        import sys

        self.verbose = verbose
        self.stream = stream or sys.stderr

    def __call__(self, event: Event) -> None:
        icon = self._ICONS.get(event.type)
        if icon is None and not self.verbose:
            return
        label = event.agent_id or event.run_id
        print(f"  {icon or '.'} {event.type:22s} {label:38s} {event.message}", file=self.stream)
