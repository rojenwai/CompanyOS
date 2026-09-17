"""Shared test helpers.

Tests run against the real repository's agent specs wherever the behaviour
under test is "does this work on the actual 107 definitions", and against a
tiny synthetic spec tree wherever determinism matters more than realism.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from companyos.config import ProviderConfig, RuntimeConfig, RuntimeLimits
from companyos.models import Task, TaskGraph
from companyos.observability import EventBus
from companyos.providers.mock import MockProvider
from companyos.registry import AgentRegistry

REPO_ROOT = Path(__file__).resolve().parents[2]

_registry_cache: AgentRegistry | None = None


def repo_registry() -> AgentRegistry:
    """The real registry, parsed once and shared across tests."""
    global _registry_cache
    if _registry_cache is None:
        _registry_cache = AgentRegistry.discover(REPO_ROOT)
    return _registry_cache


def config(**overrides: Any) -> RuntimeConfig:
    """A runtime config pointed at the real repo, with test-friendly limits."""
    limits = RuntimeLimits(
        **{
            **{
                "max_agents": 8,
                "max_parallel": 4,
                "max_iterations": 2,
                "task_timeout_s": 5.0,
                "run_timeout_s": 20.0,
            },
            **overrides.pop("limits", {}),
        }
    )
    return RuntimeConfig(
        root=overrides.pop("root", REPO_ROOT),
        provider=ProviderConfig(name="mock"),
        limits=limits,
        **overrides,
    )


def bus() -> EventBus:
    return EventBus()


def provider(**kwargs: Any) -> MockProvider:
    return MockProvider(ProviderConfig(name="mock"), **kwargs)


def run(coro):
    """Run a coroutine to completion."""
    return asyncio.run(coro)


def task(objective: str, *, deps: tuple[str, ...] = (), **kwargs: Any) -> Task:
    t = Task(objective=objective, **kwargs)
    t.dependencies = list(deps)
    return t


def linear_graph(*objectives: str) -> TaskGraph:
    """A -> B -> C. Every node depends on the one before it."""
    graph = TaskGraph()
    previous: str | None = None
    for objective in objectives:
        node = graph.add(Task(objective=objective))
        if previous:
            node.dependencies.append(previous)
        previous = node.id
    graph.validate()
    return graph


def parallel_graph(*objectives: str) -> TaskGraph:
    """Independent nodes with no dependencies between them."""
    graph = TaskGraph([Task(objective=o) for o in objectives])
    graph.validate()
    return graph


# --- a minimal synthetic spec tree --------------------------------------------

_SPEC = """# {name}

**Division:** {division} · **Reports to:** [{reports_to}]({reports_to_file})

## 1. Mission
{mission}

## 2. Responsibilities
{responsibilities}

## 3. Inputs
Task assignments.

## 4. Outputs
A deliverable.

## 5. Tools
{tools}

## 6. Workflows
1. Do the work. 2. Check it.

## 7. Collaboration rules
Works with other agents.

## 8. Escalation rules
Escalates when blocked.

## 9. Quality standards
Specific and evidence-backed.

## 10. KPIs
Throughput.

## 11. Review requirements
Reviewed by the Reviewer.
"""


def write_spec(
    root: Path,
    division: str,
    slug: str,
    *,
    name: str | None = None,
    mission: str = "Do one thing well.",
    responsibilities: str = "- Own the deliverable",
    tools: str = "Read access to memory.",
    reports_to: str = "CEO Agent",
) -> Path:
    """Write one synthetic agent spec, in the repository's own 11-section shape."""
    directory = root / "ai" / "agents" / division
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{slug}.md"
    path.write_text(
        _SPEC.format(
            name=name or slug.replace("-", " ").title(),
            division=division,
            reports_to=reports_to,
            reports_to_file="../../orchestration/ceo-agent.md",
            mission=mission,
            responsibilities=responsibilities,
            tools=tools,
        ),
        encoding="utf-8",
    )
    return path


def synthetic_repo(root: Path) -> Path:
    """Build a minimal but complete spec tree: a CEO, a planner, a decomposer,
    a reviewer, and two specialists."""
    kernel = root / "ai" / "orchestration"
    kernel.mkdir(parents=True, exist_ok=True)
    (root / "ai" / "memory").mkdir(parents=True, exist_ok=True)

    for slug, name, mission in (
        ("ceo-agent", "CEO Agent", "Orchestrate the company. Delegates, never implements."),
        ("planner", "Planner Agent", "Turn an objective into a plan. Decompose subtasks."),
        ("task-decomposer", "Task Decomposer Agent", "Split a plan into subtasks with dependencies."),
        ("reviewer", "Reviewer Agent", "Verify correctness and quality. Never assumes the author is correct."),
    ):
        (kernel / f"{slug}.md").write_text(
            _SPEC.format(
                name=name,
                division="Orchestration",
                reports_to="CEO Agent",
                reports_to_file="ceo-agent.md",
                mission=mission,
                responsibilities="- Kernel duties",
                tools="Read access to memory.",
            ),
            encoding="utf-8",
        )

    write_spec(
        root,
        "engineering",
        "backend-engineer",
        name="Backend Engineer Agent",
        mission="Build reliable server-side services, endpoints, and authentication.",
        responsibilities="- APIs, endpoints, backend services, authentication, authorization",
        tools="Code execution; test runners.",
    )
    write_spec(
        root,
        "security",
        "security-architect-agent",
        name="Security Architect Agent",
        mission="Threat model systems and design security controls.",
        responsibilities="- Build threat models (STRIDE/attack trees); specify security controls",
        tools="Threat-modeling tools; read access to memory.",
    )
    return root
