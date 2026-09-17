"""Per-run scratchpad: temporary task state that must never become company memory.

``ai/memory/README.md`` draws the line as "session facts never leak into company
memory without promotion". This class is the session side of that line. It is
created per run, held only in the run record, and discarded when the run ends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..ids import now


@dataclass
class ScratchEntry:
    key: str
    value: Any
    task_id: str = ""
    agent_id: str = ""
    created_at: float = field(default_factory=now)


class RunScratchpad:
    """Ephemeral key/value state scoped to one run.

    Writes are namespaced by task so one agent instance cannot silently clobber
    another's working state.
    """

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self._entries: dict[str, ScratchEntry] = {}

    def put(self, key: str, value: Any, *, task_id: str = "", agent_id: str = "") -> None:
        scoped = f"{task_id}:{key}" if task_id else key
        self._entries[scoped] = ScratchEntry(key, value, task_id, agent_id)

    def get(self, key: str, *, task_id: str = "", default: Any = None) -> Any:
        scoped = f"{task_id}:{key}" if task_id else key
        entry = self._entries.get(scoped)
        return default if entry is None else entry.value

    def for_task(self, task_id: str) -> dict[str, Any]:
        return {e.key: e.value for e in self._entries.values() if e.task_id == task_id}

    def keys(self) -> list[str]:
        return sorted(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "entries": [
                {"key": e.key, "task_id": e.task_id, "agent_id": e.agent_id}
                for e in self._entries.values()
            ],
        }
