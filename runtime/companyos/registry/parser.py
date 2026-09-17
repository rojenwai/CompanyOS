"""Parse a CompanyOS Markdown agent spec into an :class:`AgentDefinition`.

The specs are the source of truth. This module reads them; it never writes
them, and it tolerates the two header dialects that exist in the repository:

    **Division:** Engineering · **Reports to:** [Software Architect](x.md)

and

    **Division:** Engineering
    **Reports to:** [Software Architect](x.md)

Specs with neither (e.g. ``ai/agents/security/*``) fall back to the folder name.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..errors import RegistryError
from . import capabilities as caps
from .definition import AgentDefinition, AgentKind

_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
_SECTION = re.compile(r"^##\s*(\d+)\.\s*(.+?)\s*$", re.M)
_DIVISION = re.compile(r"\*\*Division:\*\*\s*([^\n·|]+)", re.I)
_REPORTS_TO = re.compile(r"\*\*Reports to:\*\*\s*([^\n·|]+)", re.I)
_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

#: Phrases in a spec's section 5 -> runtime tool names.
#: Unmapped phrases are kept in ``raw_tools_text`` rather than silently dropped.
_TOOL_ALIASES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("read access", "read tools", "diff/read", "read/write", "architecture review"), "read_spec"),
    (("search", "retrieval", "knowledge base", "threat-modeling tools"), "search_specs"),
    (("memory",), "recall_memory"),
    (("code execution", "test runner", "test runners", "coverage tools", "ci pipeline",
      "static analysis", "dependency scanner", "dependency scanners"), "run_checks"),
    (("planning", "graph/dependency", "dependency modeling"), "plan_tasks"),
    (("delegation", "approval engine"), "delegate"),
)

#: An agent whose spec says it delegates rather than implements.
_DELEGATION_MARKERS = (
    "delegates, never implements",
    "does not: write production code",
    "does **not**: write production code",
    "never performing specialist implementation",
    "it delegates",
    "does not write production code",
)

_REVIEW_CONCERNS = {
    "security": ("security", "threat", "vulnerab", "owasp"),
    "quality": ("test", "coverage", "qa"),
    "documentation": ("documentation", "docs", "readme"),
    "correctness": ("correctness", "readability", "maintainability", "edge case"),
}


def parse_agent_spec(path: Path, *, root: Path | None = None) -> AgentDefinition:
    """Read one ``.md`` spec and return its parsed definition."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - filesystem failure
        raise RegistryError(f"cannot read agent spec {path}: {exc}") from exc

    sections = _parse_sections(text)
    if not sections:
        raise RegistryError(f"{path}: no numbered sections found; not an agent spec")

    division = _parse_division(text, path)
    name = _parse_name(text, path)
    kind = _classify(path, name, text)
    tools, prohibited, raw_tools = _parse_tools(sections.get(5, ""))

    # The title is the strongest single signal an agent carries -- "Problem
    # Discovery Agent" states its capability more plainly than any sentence in
    # its body -- so name and slug are weighted alongside the spec text.
    slug = path.stem
    signal = "\n".join(
        [name, slug.replace("-", " "), *(sections.get(n, "") for n in (1, 2, 4, 5, 6))]
    )
    scores = caps.extract(signal)
    # Identity capabilities: every agent is addressable by division and by role,
    # so a planner can ask for `division.security` or `role.backend-engineer`.
    scores.setdefault(f"division.{division}", 2)
    scores.setdefault(f"role.{slug}", 3)

    return AgentDefinition(
        id=f"{division}/{slug}",
        name=name,
        division=division,
        kind=kind,
        source_path=path if root is None else _relative(path, root),
        reports_to=_parse_reports_to(text),
        sections=sections,
        capabilities=tuple(sorted(scores, key=lambda c: (-scores[c], c))),
        capability_scores=scores,
        tools=tools,
        prohibited_tools=prohibited,
        raw_tools_text=raw_tools,
        can_execute_independently=kind not in (AgentKind.EXECUTIVE, AgentKind.ORCHESTRATION)
        and not _is_delegator(text),
        reviews_for=(
            _review_concerns(sections) if kind == AgentKind.REVIEWER else ()
        ),
        supervises=_parse_supervises(sections.get(2, "")),
    )


def _relative(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:  # pragma: no cover - spec outside the root
        return path


def _parse_sections(text: str) -> dict[int, str]:
    """Split on ``## N. Title`` headers, returning ``{number: body}``."""
    matches = list(_SECTION.finditer(text))
    sections: dict[int, str] = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[start:end].strip()
    return sections


def _parse_name(text: str, path: Path) -> str:
    for match in _H1.finditer(text):
        title = match.group(1).strip()
        if title.lower().startswith("agent:"):
            title = title.split(":", 1)[1].strip()
        if title and title.lower() != "agent template":
            return title
    return path.stem.replace("-", " ").title()


def _parse_division(text: str, path: Path) -> str:
    """The owning division.

    The folder name is canonical -- it matches ``handbook/departments/`` one for
    one. The ``**Division:**`` line is only consulted for a spec that sits
    outside a division folder, because its wording varies ("Post-Launch /
    Maintenance", "AI", "People").
    """
    folder = path.parent.name
    if folder not in ("agents", "."):
        return folder

    match = _DIVISION.search(text)
    if match:
        value = _strip_links(match.group(1)).strip().strip("*").strip()
        if value and "<" not in value:
            first = value.split("/")[0].strip()
            slug = re.sub(r"[^a-z0-9]+", "-", first.lower()).strip("-")
            return {"ai": "ai-engineering", "people": "hr", "business": "strategy"}.get(slug, slug)
    return folder


def _parse_supervises(section: str) -> tuple[str, ...]:
    """Divisions an executive spec claims to supervise.

    The C-suite specs state this in prose -- the CTO's reads "Supervises the
    Engineering, DevOps, AI, Hardware, and Post-Launch divisions" -- so the
    reporting hierarchy in the Agent Map comes from the specs themselves rather
    than a table maintained in code.
    """
    match = re.search(r"supervises?\s+(?:the\s+)?(.+?)\s+divisions?", section, re.I | re.S)
    if not match:
        return ()
    fragment = _strip_links(match.group(1))
    parts = re.split(r",|\band\b|/|·", fragment)
    out: list[str] = []
    for part in parts:
        slug = re.sub(r"[^a-z0-9]+", "-", part.strip().lower()).strip("-")
        slug = {"ai": "ai-engineering", "people": "hr", "business": "strategy"}.get(slug, slug)
        if slug and slug not in out:
            out.append(slug)
    return tuple(out)


def _parse_reports_to(text: str) -> str | None:
    match = _REPORTS_TO.search(text)
    if not match:
        return None
    value = _strip_links(match.group(1)).strip().strip("*").strip(" .")
    return value or None


def _strip_links(value: str) -> str:
    return _MD_LINK.sub(r"\1", value)


def _classify(path: Path, name: str, text: str) -> str:
    folder = path.parent.name
    lowered = name.lower()
    if "reviewer" in lowered or "critic" in lowered:
        return AgentKind.REVIEWER
    if folder == "orchestration":
        return AgentKind.ORCHESTRATION
    if folder == "executive":
        return AgentKind.EXECUTIVE
    return AgentKind.SPECIALIST


def _is_delegator(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in _DELEGATION_MARKERS)


def _parse_tools(section: str) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    """Map the free-text tools section onto runtime tool names.

    Anything the spec explicitly forbids ("never", "prohibited", "does not use")
    lands in ``prohibited`` and is subtracted from the granted set.
    """
    lowered = section.lower()
    granted: list[str] = []
    for phrases, tool in _TOOL_ALIASES:
        if any(phrase in lowered for phrase in phrases) and tool not in granted:
            granted.append(tool)

    prohibited: list[str] = []
    for sentence in re.split(r"[.;\n]", lowered):
        if not any(k in sentence for k in ("never", "prohibit", "does not use", "not permitted")):
            continue
        for phrases, tool in _TOOL_ALIASES:
            if any(phrase in sentence for phrase in phrases) and tool not in prohibited:
                prohibited.append(tool)

    granted = [t for t in granted if t not in prohibited]
    return tuple(granted), tuple(prohibited), section.strip()


def _review_concerns(sections: dict[int, str]) -> tuple[str, ...]:
    """What a reviewer is accountable for, from its mission and responsibilities.

    Only sections 1 and 2 are read. The general Reviewer's collaboration rules
    say it "hands security concerns to the Security Reviewer" -- mentioning
    another reviewer's concern is a hand-off, not a claim to it.
    """
    lowered = f"{sections.get(1, '')}\n{sections.get(2, '')}".lower()
    return tuple(
        concern
        for concern, markers in _REVIEW_CONCERNS.items()
        if any(m in lowered for m in markers)
    )
