"""CompanyOS runtime: dynamic multi-agent orchestration over the Markdown agent specs.

The 107 specs in ``ai/agents/`` are *agent definitions* -- templates. This
package selects the ones a task needs, spawns temporary instances of them, runs
independent work in parallel, reviews the results, and synthesizes an answer.

Quick start::

    from companyos import Orchestrator, RuntimeConfig

    config = RuntimeConfig.load()                       # finds the repo root
    run = Orchestrator(config).run_sync("Design and implement authentication.")
    print(run.final_output)
    print(Orchestrator(config).agent_map(run))
"""

from .config import Budget, ProviderConfig, RuntimeConfig, RuntimeLimits, find_repo_root
from .models import AgentResult, ReviewReport, RunRecord, Task, TaskGraph, Usage
from .observability import EventBus, EventType
from .orchestration import Orchestrator, build_agent_map, render_tree, run_request
from .registry import AgentDefinition, AgentRegistry
from .status import RunStatus, TaskStatus, Verdict

__version__ = "0.1.0"

__all__ = [
    "AgentDefinition",
    "AgentRegistry",
    "AgentResult",
    "Budget",
    "EventBus",
    "EventType",
    "Orchestrator",
    "ProviderConfig",
    "ReviewReport",
    "RunRecord",
    "RunStatus",
    "RuntimeConfig",
    "RuntimeLimits",
    "Task",
    "TaskGraph",
    "TaskStatus",
    "Usage",
    "Verdict",
    "__version__",
    "build_agent_map",
    "find_repo_root",
    "render_tree",
    "run_request",
]
