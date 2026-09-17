"""Runtime configuration and the safeguards that keep a run bounded."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, replace
from pathlib import Path

from .errors import ConfigError, LimitExceeded

#: Marker directories that identify a CompanyOS repository root.
_ROOT_MARKERS = (("ai", "agents"), ("ai", "orchestration"))


def find_repo_root(start: Path | str | None = None) -> Path:
    """Walk upwards from ``start`` until the CompanyOS spec tree is found.

    ``COMPANYOS_ROOT`` overrides the search. Raises :class:`ConfigError` if no
    root is found, because a runtime with no agent definitions is useless.
    """
    env = os.environ.get("COMPANYOS_ROOT")
    if env:
        root = Path(env).expanduser().resolve()
        if not _is_root(root):
            raise ConfigError(f"COMPANYOS_ROOT={root} does not contain ai/agents/")
        return root

    here = Path(start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if _is_root(candidate):
            return candidate
    raise ConfigError(
        f"no CompanyOS root found above {here}; set COMPANYOS_ROOT to the repository root"
    )


def _is_root(path: Path) -> bool:
    return all((path.joinpath(*parts)).is_dir() for parts in _ROOT_MARKERS)


@dataclass(frozen=True)
class RuntimeLimits:
    """Hard safeguards. Every one of these exists to stop runaway spawning."""

    max_agents: int = 12
    """Total agent instances a single run may spawn, reviewers included."""

    max_depth: int = 3
    """Maximum task-tree depth. Root objective is depth 0."""

    max_iterations: int = 2
    """Plan -> execute -> review -> replan cycles before the run finalizes."""

    max_parallel: int = 4
    """Agent instances executing concurrently."""

    max_attempts_per_task: int = 2
    """Attempts for one task, including the first."""

    task_timeout_s: float = 120.0
    run_timeout_s: float = 600.0

    max_total_tokens: int = 400_000
    """Combined prompt+completion tokens across the whole run."""

    max_tool_calls_per_agent: int = 8
    max_context_chars: int = 24_000
    """Upper bound on one agent's assembled context, per context-management.md."""

    def validate(self) -> None:
        for name in (
            "max_agents",
            "max_depth",
            "max_iterations",
            "max_parallel",
            "max_attempts_per_task",
        ):
            if getattr(self, name) < 1:
                raise ConfigError(f"{name} must be >= 1")
        if self.task_timeout_s <= 0 or self.run_timeout_s <= 0:
            raise ConfigError("timeouts must be positive")


@dataclass
class Budget:
    """Mutable spend counters for one run, checked against :class:`RuntimeLimits`."""

    limits: RuntimeLimits
    agents_spawned: int = 0
    tokens_used: int = 0
    iterations: int = 0

    def charge_agent(self) -> None:
        if self.agents_spawned + 1 > self.limits.max_agents:
            raise LimitExceeded("max_agents", self.agents_spawned + 1, self.limits.max_agents)
        self.agents_spawned += 1

    def charge_tokens(self, n: int) -> None:
        self.tokens_used += max(0, n)
        if self.tokens_used > self.limits.max_total_tokens:
            raise LimitExceeded(
                "max_total_tokens", self.tokens_used, self.limits.max_total_tokens
            )

    def charge_iteration(self) -> None:
        if self.iterations + 1 > self.limits.max_iterations:
            raise LimitExceeded(
                "max_iterations", self.iterations + 1, self.limits.max_iterations
            )
        self.iterations += 1

    def agents_remaining(self) -> int:
        return max(0, self.limits.max_agents - self.agents_spawned)

    def snapshot(self) -> dict:
        return {
            "agents_spawned": self.agents_spawned,
            "tokens_used": self.tokens_used,
            "iterations": self.iterations,
            "limits": {
                "max_agents": self.limits.max_agents,
                "max_depth": self.limits.max_depth,
                "max_iterations": self.limits.max_iterations,
                "max_parallel": self.limits.max_parallel,
                "max_total_tokens": self.limits.max_total_tokens,
            },
        }


@dataclass(frozen=True)
class ProviderConfig:
    """Which model answers, and how. No provider-specific logic leaks upward."""

    name: str = "mock"
    model: str = ""
    api_key_env: str = ""
    base_url: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096
    extra: dict = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeConfig:
    """Everything the runtime needs to execute a request."""

    root: Path
    provider: ProviderConfig = field(default_factory=ProviderConfig)
    limits: RuntimeLimits = field(default_factory=RuntimeLimits)

    #: Tools every spawned agent may use unless its spec narrows them further.
    default_tools: tuple[str, ...] = ("read_spec", "search_specs", "recall_memory")

    #: Tools no dynamically spawned agent may ever receive, whatever its spec says.
    denied_tools: tuple[str, ...] = ("shell", "write_file", "http_request")

    #: Directories a sandboxed file tool may read, relative to ``root``.
    readable_dirs: tuple[str, ...] = ("ai", "handbook", "starter-kits")

    #: Where run traces and artifacts are written.
    run_dir: Path | None = None

    #: When false, agent memory writes stay in the run scratchpad and are only
    #: *proposed* for promotion to persistent organizational memory.
    allow_memory_promotion: bool = False

    def __post_init__(self) -> None:
        self.limits.validate()

    @property
    def traces_dir(self) -> Path:
        return (self.run_dir or (self.root / ".companyos" / "runs")).resolve()

    def with_provider(self, **kw) -> "RuntimeConfig":
        return replace(self, provider=replace(self.provider, **kw))

    # -- construction ----------------------------------------------------------

    @classmethod
    def load(
        cls,
        root: Path | str | None = None,
        config_file: Path | str | None = None,
        **overrides,
    ) -> "RuntimeConfig":
        """Build a config from (in order) defaults, a JSON file, then kwargs."""
        resolved_root = Path(root).resolve() if root else find_repo_root()
        data: dict = {}

        path = Path(config_file) if config_file else resolved_root / "companyos.json"
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ConfigError(f"{path}: invalid JSON ({exc})") from exc

        provider = ProviderConfig(**{**data.get("provider", {}), **overrides.pop("provider", {})})
        limits = RuntimeLimits(**{**data.get("limits", {}), **overrides.pop("limits", {})})

        known = {"default_tools", "denied_tools", "readable_dirs", "allow_memory_promotion"}
        kwargs = {k: tuple(v) if isinstance(v, list) else v
                  for k, v in data.items() if k in known}
        kwargs.update(overrides)
        if "run_dir" in kwargs and kwargs["run_dir"] is not None:
            kwargs["run_dir"] = Path(kwargs["run_dir"])

        return cls(root=resolved_root, provider=provider, limits=limits, **kwargs)
