"""File-backed memory over the existing ``ai/memory/`` documents.

CompanyOS already defines 14 memory types as Markdown. This store indexes them
as they are -- it does not restructure or duplicate them -- so retrieval works
against the organization's real written memory on a fresh clone.

Chunking is by heading, because that is the unit the documents are written in.
Ranking follows ``ai/memory/retrieval.md``: relevance first, then recency, then
source reliability.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from ..ids import now
from ..registry import capabilities as caps
from .store import MemoryProposal, MemoryRecord, MemoryStore, dedupe

_HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.M)

#: Stores whose content is durable company knowledge rank above volatile ones.
_RELIABILITY = {
    "company-memory": 1.0,
    "decision-memory": 0.95,
    "architecture-memory": 0.9,
    "knowledge-base": 0.9,
    "project-memory": 0.8,
    "lessons-learned": 0.8,
    "department-memory": 0.75,
    "research-memory": 0.7,
    "customer-memory": 0.7,
    "documentation-memory": 0.7,
    "prompt-memory": 0.6,
    "user-memory": 0.6,
    "meeting-memory": 0.5,
    "session-memory": 0.4,
}
_DEFAULT_RELIABILITY = 0.5


class FileMemoryStore(MemoryStore):
    """Read-only retrieval over ``ai/memory/``, with a gated write path."""

    def __init__(self, root: Path | str, *, allow_promotion: bool = False) -> None:
        self.root = Path(root).resolve()
        self.memory_dir = self.root / "ai" / "memory"
        self.allow_promotion = allow_promotion
        self._records: list[MemoryRecord] = []
        self._proposals: list[MemoryProposal] = []
        self._idf: dict[str, float] = {}
        self._tokens: dict[str, set[str]] = {}
        self._load()

    # -- indexing --------------------------------------------------------------

    def _load(self) -> None:
        if not self.memory_dir.is_dir():
            return
        for path in sorted(self.memory_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            store = path.stem
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:  # pragma: no cover - unreadable file
                continue
            mtime = path.stat().st_mtime
            for anchor, body in _chunks(text):
                if not body.strip():
                    continue
                self._records.append(
                    MemoryRecord(
                        id=f"{store}#{anchor}",
                        store=store,
                        text=body.strip(),
                        source=f"ai/memory/{path.name}#{anchor}",
                        tags=_tags_for(store, anchor),
                        confidence=_RELIABILITY.get(store, _DEFAULT_RELIABILITY),
                        timestamp=mtime,
                    )
                )
        self._build_index()

    def _build_index(self) -> None:
        import math

        self._tokens = {r.id: set(caps.tokenize(f"{r.id} {r.text}")) for r in self._records}
        n = max(1, len(self._tokens))
        df: dict[str, int] = {}
        for tokens in self._tokens.values():
            for token in tokens:
                df[token] = df.get(token, 0) + 1
        self._idf = {t: math.log(1 + n / (1 + c)) for t, c in df.items()}

    # -- MemoryStore -----------------------------------------------------------

    @property
    def stores(self) -> list[str]:
        return sorted({r.store for r in self._records})

    def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        stores: Sequence[str] | None = None,
        min_relevance: float = 0.05,
    ) -> list[MemoryRecord]:
        query_tokens = set(caps.tokenize(query))
        if not query_tokens or not self._records:
            return []

        allowed = set(stores) if stores else None
        possible = sum(self._idf.get(t, 0.0) for t in query_tokens) or 1.0
        newest = max((r.timestamp for r in self._records), default=now()) or 1.0

        scored: list[MemoryRecord] = []
        for record in self._records:
            if allowed is not None and record.store not in allowed:
                continue
            overlap = query_tokens & self._tokens.get(record.id, set())
            if not overlap:
                continue
            relevance = sum(self._idf.get(t, 0.0) for t in overlap) / possible
            if relevance < min_relevance:
                continue
            # relevance, then recency, then source reliability (retrieval.md)
            recency = 0.5 + 0.5 * (record.timestamp / newest if newest else 1.0)
            ranked = relevance * (0.7 + 0.2 * recency + 0.1 * record.confidence)
            scored.append(
                MemoryRecord(
                    id=record.id,
                    store=record.store,
                    text=record.text,
                    source=record.source,
                    tags=record.tags,
                    confidence=record.confidence,
                    timestamp=record.timestamp,
                    relevance=ranked,
                )
            )
        return dedupe(scored)[:k]

    def propose(self, proposal: MemoryProposal) -> MemoryProposal:
        reason = proposal.validate()
        if reason:
            proposal.rejected_reason = reason
        self._proposals.append(proposal)
        return proposal

    def proposals(self) -> list[MemoryProposal]:
        return list(self._proposals)

    def promote(self, proposal: MemoryProposal) -> MemoryProposal:
        """Append a validated proposal to its memory document.

        Refuses unless the runtime was configured with
        ``allow_memory_promotion``. This is the only code path in the runtime
        that writes into the specification repository.
        """
        if not self.allow_promotion:
            proposal.rejected_reason = "promotion disabled by runtime policy"
            return proposal
        reason = proposal.validate()
        if reason:
            proposal.rejected_reason = reason
            return proposal

        target = self.memory_dir / f"{proposal.store}.md"
        if not target.is_file():
            proposal.rejected_reason = f"unknown memory store {proposal.store!r}"
            return proposal

        from ..ids import iso

        entry = (
            f"\n### {iso(proposal.created_at)} - {proposal.agent_id or 'runtime'}\n\n"
            f"{proposal.text.strip()}\n\n"
            f"Source: {proposal.source} · Tags: {', '.join(proposal.tags)} · "
            f"Run: {proposal.run_id or 'n/a'}\n"
        )
        with target.open("a", encoding="utf-8") as fh:
            fh.write(entry)
        proposal.promoted = True
        return proposal


def _chunks(text: str) -> list[tuple[str, str]]:
    """Split a memory document into ``(anchor, body)`` pairs by heading."""
    matches = list(_HEADING.finditer(text))
    if not matches:
        return [("document", text)]
    out: list[tuple[str, str]] = []
    preamble = text[: matches[0].start()].strip()
    if preamble:
        out.append(("intro", preamble))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        anchor = re.sub(r"[^a-z0-9]+", "-", match.group(2).lower()).strip("-")
        out.append((anchor or f"section-{i}", text[match.start() : end]))
    return out


def _tags_for(store: str, anchor: str) -> tuple[str, ...]:
    parts = [store.replace("-memory", "").replace("-", " ")]
    parts += anchor.split("-")
    return tuple(sorted({p for p in parts if len(p) > 2}))
