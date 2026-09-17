"""Exception hierarchy for the CompanyOS runtime.

Every failure a run can hit is one of these, so the orchestrator can decide
between "degrade and keep going" and "stop the run" without string matching.
"""

from __future__ import annotations


class CompanyOSError(Exception):
    """Base class for every runtime error."""


# --- configuration / registry -------------------------------------------------


class ConfigError(CompanyOSError):
    """The runtime was configured with something it cannot use."""


class RegistryError(CompanyOSError):
    """Agent definitions could not be discovered or parsed."""


class AgentNotFoundError(RegistryError):
    """No agent definition matches the requested id."""


class NoSuitableAgentError(RegistryError):
    """Selection ran but nothing cleared the score threshold."""


# --- task graph ---------------------------------------------------------------


class GraphError(CompanyOSError):
    """The task graph is malformed."""


class CyclicDependencyError(GraphError):
    """Task dependencies form a cycle; the DAG cannot be scheduled."""


class MalformedTaskError(GraphError):
    """A task is missing fields the scheduler requires."""


# --- execution ----------------------------------------------------------------


class ExecutionError(CompanyOSError):
    """An agent instance failed to produce a usable result."""


class AgentTimeoutError(ExecutionError):
    """The agent instance exceeded its task timeout."""


class DependencyFailedError(ExecutionError):
    """A required upstream task failed, so this one cannot run."""


class InvalidOutputError(ExecutionError):
    """The agent returned output the runtime could not parse or validate."""


# --- providers ----------------------------------------------------------------


class ProviderError(CompanyOSError):
    """The LLM provider failed."""


class ProviderUnavailableError(ProviderError):
    """The provider is not installed, not configured, or unreachable."""


# --- tools / policy -----------------------------------------------------------


class ToolError(CompanyOSError):
    """A tool call failed."""


class ToolPermissionError(ToolError):
    """The agent is not permitted to use this tool (see tools/policy.py)."""


class ToolSandboxError(ToolError):
    """The tool call tried to escape its sandbox (path, host, or secret)."""


# --- budget / safety ----------------------------------------------------------


class LimitExceeded(CompanyOSError):
    """A runtime safeguard tripped. Carries the limit that was hit."""

    def __init__(self, limit: str, value: object, cap: object) -> None:
        super().__init__(f"limit '{limit}' exceeded: {value} > {cap}")
        self.limit = limit
        self.value = value
        self.cap = cap


class RunCancelled(CompanyOSError):
    """The run was cancelled by its caller."""
