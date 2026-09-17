"""The built-in tool set.

Read-only by design. The runtime ships no shell, no network, and no filesystem
write tool, because a dynamically spawned agent acting on model-generated
instructions must not be able to reach any of them. ``shell``, ``write_file``
and ``http_request`` exist here only as explicit refusals, so that a spec
mentioning them produces a clear denial rather than a confusing "unknown tool".
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from ..errors import ToolError, ToolSandboxError
from . import Tool, ToolContext

_MAX_READ_CHARS = 20_000
_MAX_HITS = 20
_TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml"}


# --- sandbox ------------------------------------------------------------------


def _safe_path(raw: str, context: ToolContext) -> Path:
    """Resolve a caller-supplied path, or refuse.

    Blocks absolute paths, traversal out of the repository, symlinks that point
    outside it, directories not on the readable list, and non-text files.
    """
    if not raw or not raw.strip():
        raise ToolSandboxError("path is required")
    candidate = Path(raw.strip().replace("\\", "/"))
    # `root` catches a leading slash, which Windows does not consider absolute
    # (it has no drive) but which must still be refused everywhere.
    if candidate.is_absolute() or candidate.drive or candidate.root:
        raise ToolSandboxError(f"absolute paths are not permitted: {raw!r}")

    root = context.root.resolve()
    resolved = (root / candidate).resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        raise ToolSandboxError(f"path escapes the repository sandbox: {raw!r}") from None

    allowed = context.readable_dirs or ()
    if allowed and relative.parts and relative.parts[0] not in allowed:
        raise ToolSandboxError(
            f"{relative.as_posix()!r} is outside the readable set ({', '.join(allowed)})"
        )
    if resolved.is_file() and resolved.suffix.lower() not in _TEXT_SUFFIXES:
        raise ToolSandboxError(f"only text specs may be read, not {resolved.suffix!r}")
    return resolved


# --- handlers -----------------------------------------------------------------


def _read_spec(arguments: Mapping[str, Any], context: ToolContext) -> str:
    path = _safe_path(str(arguments.get("path", "")), context)
    if not path.is_file():
        raise ToolError(f"no such file: {arguments.get('path')!r}")
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > _MAX_READ_CHARS:
        text = text[:_MAX_READ_CHARS] + "\n\n[truncated]"
    return text


def _search_specs(arguments: Mapping[str, Any], context: ToolContext) -> str:
    query = str(arguments.get("query", "")).strip()
    if len(query) < 3:
        raise ToolError("query must be at least 3 characters")
    limit = min(int(arguments.get("limit", 10) or 10), _MAX_HITS)

    try:
        pattern = re.compile(re.escape(query), re.I)
    except re.error as exc:  # pragma: no cover - escaped input cannot fail
        raise ToolError(f"bad query: {exc}") from exc

    hits: list[str] = []
    for directory in context.readable_dirs or ("ai",):
        base = context.root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:  # pragma: no cover
                continue
            match = pattern.search(text)
            if not match:
                continue
            line_no = text[: match.start()].count("\n") + 1
            line = text.splitlines()[line_no - 1].strip()
            hits.append(f"{path.relative_to(context.root).as_posix()}:{line_no}: {line[:160]}")
            if len(hits) >= limit:
                return "\n".join(hits)
    return "\n".join(hits) if hits else "no matches"


def _recall_memory(arguments: Mapping[str, Any], context: ToolContext) -> str:
    if context.memory is None:
        raise ToolError("no memory store is attached to this run")
    query = str(arguments.get("query", "")).strip()
    if not query:
        raise ToolError("query is required")
    k = min(int(arguments.get("k", 3) or 3), 8)
    records = context.memory.retrieve(query, k=k)
    if not records:
        # retrieval.md: say so rather than returning a low-confidence guess.
        return "no reliable source"
    return "\n\n".join(
        f"[{r.store} · relevance {r.relevance:.2f} · source {r.source}]\n{r.text[:800]}"
        for r in records
    )


def _remember(arguments: Mapping[str, Any], context: ToolContext) -> str:
    """Propose a memory write. Never writes persistent memory directly."""
    if context.memory is None:
        raise ToolError("no memory store is attached to this run")
    from ..memory.store import MemoryProposal

    proposal = context.memory.propose(
        MemoryProposal(
            store=str(arguments.get("store", "session-memory")),
            text=str(arguments.get("text", "")),
            source=f"run:{context.run_id} task:{context.task_id} agent:{context.agent_id}",
            tags=tuple(str(t) for t in (arguments.get("tags") or ())),
            agent_id=context.agent_id,
            task_id=context.task_id,
            run_id=context.run_id,
        )
    )
    if proposal.rejected_reason:
        return f"proposal rejected: {proposal.rejected_reason}"
    return (
        f"proposal {proposal.id} recorded for {proposal.store}; "
        "it becomes organizational memory only after promotion"
    )


def _refuse(name: str, reason: str):
    def handler(arguments: Mapping[str, Any], context: ToolContext) -> str:
        raise ToolSandboxError(f"{name} is not available to spawned agents: {reason}")

    return handler


# --- the set ------------------------------------------------------------------

BUILTIN_TOOLS: tuple[Tool, ...] = (
    Tool(
        name="read_spec",
        description=(
            "Read one Markdown document from the CompanyOS repository "
            "(handbook, ai, or starter-kits). Relative paths only."
        ),
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Repo-relative path, e.g. ai/agents/engineering/backend-engineer.md",
                }
            },
            "required": ["path"],
        },
        handler=_read_spec,
    ),
    Tool(
        name="search_specs",
        description="Full-text search across the CompanyOS documentation.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": _MAX_HITS},
            },
            "required": ["query"],
        },
        handler=_search_specs,
    ),
    Tool(
        name="recall_memory",
        description=(
            "Retrieve relevant organizational memory. Returns 'no reliable source' "
            "when nothing authoritative matches."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "k": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["query"],
        },
        handler=_recall_memory,
    ),
    Tool(
        name="remember",
        description=(
            "Propose a durable memory write. The proposal is reviewed before it "
            "can become organizational memory."
        ),
        parameters={
            "type": "object",
            "properties": {
                "store": {"type": "string"},
                "text": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["store", "text", "tags"],
        },
        handler=_remember,
        mutating=True,
    ),
    Tool(
        name="shell",
        description="Not available.",
        parameters={"type": "object", "properties": {}},
        handler=_refuse("shell", "the local runtime executes no commands"),
        mutating=True,
    ),
    Tool(
        name="write_file",
        description="Not available.",
        parameters={"type": "object", "properties": {}},
        handler=_refuse("write_file", "agents return artifacts; they do not write to disk"),
        mutating=True,
    ),
    Tool(
        name="http_request",
        description="Not available.",
        parameters={"type": "object", "properties": {}},
        handler=_refuse("http_request", "no outbound network is granted to agents"),
        mutating=True,
    ),
    Tool(
        name="run_checks",
        description="Not available.",
        parameters={"type": "object", "properties": {}},
        handler=_refuse("run_checks", "test execution is not wired into the local runtime"),
        mutating=True,
    ),
)
