"""Memory contracts.

Implements the retrieval contract written in ``ai/memory/retrieval.md``: every
result carries a source, a confidence, a timestamp, and a relevance score, and
"no reliable source" is a valid answer rather than a low-confidence guess.

The write path is deliberately two-phase. A spawned agent can only *propose* a
memory write; promotion into persistent organizational memory is a separate,
policy-gated step. That is what stops 100 temporary instances from scribbling
on company memory (``ai/orchestration/memory-manager.md``: "never writes
unvalidated memory").
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from ..ids import iso, new_id, now


@dataclass(frozen=True)
class MemoryRecord:
    """One retrieved fact."""

    id: str
    store: str
    """Which memory type it came from -- session, project, decision, ..."""

    text: str
    source: str
    """Where it came from, e.g. ``ai/memory/decision-memory.md#retention``."""

    tags: tuple[str, ...] = ()
    confidence: float = 0.5
    timestamp: float = field(default_factory=now)
    relevance: float = 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "store": self.store,
            "text": self.text,
            "source": self.source,
            "tags": list(self.tags),
            "confidence": round(self.confidence, 3),
            "relevance": round(self.relevance, 3),
            "timestamp": iso(self.timestamp),
        }


@dataclass
class MemoryProposal:
    """A pending write. Not visible to retrieval until promoted."""

    store: str
    text: str
    source: str
    tags: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: new_id("mem"))
    agent_id: str = ""
    task_id: str = ""
    run_id: str = ""
    created_at: float = field(default_factory=now)
    promoted: bool = False
    rejected_reason: str = ""

    def validate(self) -> str:
        """Return an empty string if the write is well-formed, else the reason.

        Mirrors the memory-manager's "no hallucinated memory; every stored fact
        has a source and timestamp" rule.
        """
        if not self.text.strip():
            return "empty text"
        if not self.source.strip():
            return "missing source"
        if not self.tags:
            return "untagged memory is unretrievable"
        return ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "store": self.store,
            "text": self.text,
            "source": self.source,
            "tags": list(self.tags),
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "promoted": self.promoted,
            "rejected_reason": self.rejected_reason,
            "created_at": iso(self.created_at),
        }


class MemoryStore(ABC):
    """Read/propose interface every memory backend implements."""

    @abstractmethod
    def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        stores: Sequence[str] | None = None,
        min_relevance: float = 0.05,
    ) -> list[MemoryRecord]:
        """Return the most relevant records, best first.

        An empty list means "no reliable source" and callers must say so rather
        than inventing context.
        """

    @abstractmethod
    def propose(self, proposal: MemoryProposal) -> MemoryProposal:
        """Record a candidate write. Never persists to organizational memory."""

    @abstractmethod
    def proposals(self) -> list[MemoryProposal]:
        """Every proposal made so far, promoted or not."""

    def promote(self, proposal: MemoryProposal) -> MemoryProposal:
        """Persist a validated proposal. Disabled unless policy allows it."""
        proposal.rejected_reason = "promotion disabled by runtime policy"
        return proposal

    @property
    @abstractmethod
    def stores(self) -> list[str]:
        """Names of the memory types this backend exposes."""


class NullMemoryStore(MemoryStore):
    """A store that knows nothing. Used when memory is switched off."""

    def __init__(self) -> None:
        self._proposals: list[MemoryProposal] = []

    def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        stores: Sequence[str] | None = None,
        min_relevance: float = 0.05,
    ) -> list[MemoryRecord]:
        return []

    def propose(self, proposal: MemoryProposal) -> MemoryProposal:
        self._proposals.append(proposal)
        return proposal

    def proposals(self) -> list[MemoryProposal]:
        return list(self._proposals)

    @property
    def stores(self) -> list[str]:
        return []


def dedupe(records: Iterable[MemoryRecord]) -> list[MemoryRecord]:
    """Drop records whose text repeats, keeping the most relevant copy."""
    best: dict[str, MemoryRecord] = {}
    for record in records:
        key = record.text.strip()[:200]
        if key not in best or record.relevance > best[key].relevance:
            best[key] = record
    return sorted(best.values(), key=lambda r: -r.relevance)
