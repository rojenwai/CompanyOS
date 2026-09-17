"""Agent Map: the runtime execution graph, as data.

A projection of the run record -- nothing here is computed during execution, so
the map can be rebuilt at any time from a saved run and is identical whether a
UI, the CLI, or a future API asks for it.

Node kinds:

* ``entry``      - the CEO / entry agent that received the request
* ``kernel``     - planner and decomposer
* ``supervisor`` - the executive accountable for a division. Derived from the
  specs' own reporting lines; **not a spawned instance**, which is why it
  carries ``spawned: false``. It is the chain of accountability, drawn.
* ``agent``      - a spawned specialist instance working one task
* ``reviewer``   - the review stage
* ``synthesis``  - the final composition
"""

from __future__ import annotations

from typing import Any

from ..models import RunRecord
from ..registry import AgentRegistry
from ..status import TaskStatus, spec_state


def build_agent_map(run: RunRecord, registry: AgentRegistry) -> dict:
    """Build the Agent Map document for a run."""
    nodes: list[dict] = []
    edges: list[dict] = []
    seen: set[str] = set()

    def node(node_id: str, **fields: Any) -> str:
        if node_id not in seen:
            seen.add(node_id)
            nodes.append({"id": node_id, **fields})
        return node_id

    def edge(source: str, target: str, kind: str) -> None:
        edges.append({"from": source, "to": target, "type": kind})

    # --- entry ----------------------------------------------------------------
    entry_def = registry.get(run.entry_agent) if run.entry_agent in registry else None
    root = node(
        "entry",
        parent_id=None,
        kind="entry",
        agent=entry_def.name if entry_def else run.entry_agent,
        agent_id=run.entry_agent,
        division=entry_def.division if entry_def else "orchestration",
        task=run.request,
        status=run.status.value,
        spawned=False,
        duration_s=round(run.duration_s, 3),
        errors=list(run.errors),
    )

    # --- kernel ---------------------------------------------------------------
    if run.plan:
        planner = node(
            "planner",
            parent_id=root,
            kind="kernel",
            agent="Planner",
            agent_id="orchestration/planner",
            division="orchestration",
            task=str(run.plan.get("objective", ""))[:200],
            status=TaskStatus.COMPLETED.value,
            spawned=False,
        )
        edge(root, planner, "delegates")

        decomposer = node(
            "decomposer",
            parent_id=planner,
            kind="kernel",
            agent="Task Decomposer",
            agent_id="orchestration/task-decomposer",
            division="orchestration",
            task=f"{len(run.graph)} subtask(s)",
            status=TaskStatus.COMPLETED.value,
            spawned=False,
        )
        edge(planner, decomposer, "delegates")
        branch_parent = decomposer
    else:
        branch_parent = root

    # --- supervisors + spawned specialists ------------------------------------
    for task in run.graph.topological_order():
        result = run.results.get(task.id)
        agent_id = task.assigned_agent or (result.agent_id if result else "")
        definition = registry.get(agent_id) if agent_id in registry else None

        parent = branch_parent
        if definition is not None:
            supervisor_id = registry.supervisor_for(definition)
            if supervisor_id and supervisor_id != definition.id:
                supervisor = registry.get(supervisor_id)
                parent = node(
                    f"supervisor:{supervisor.id}",
                    parent_id=branch_parent,
                    kind="supervisor",
                    agent=supervisor.name,
                    agent_id=supervisor.id,
                    division=supervisor.division,
                    task=f"Accountable for {definition.division} work in this run",
                    status="delegated",
                    spawned=False,
                )
                edge(branch_parent, parent, "delegates")

        task_node = node(
            f"task:{task.id}",
            parent_id=parent,
            kind="agent",
            agent=definition.name if definition else (agent_id or "unassigned"),
            agent_id=agent_id,
            division=definition.division if definition else "",
            task=task.objective,
            status=task.status.value,
            spec_state=spec_state(task.status),
            spawned=result is not None,
            instance_id=result.instance_id if result else None,
            attempts=task.attempts,
            duration_s=(
                round(task.duration_s, 3) if task.duration_s is not None else None
            ),
            started_at=task.started_at,
            errors=([task.error] if task.error else []) + (result.errors if result else []),
            usage=result.usage.to_dict() if result else None,
            provider=result.provider if result else None,
            model=result.model if result else None,
            tool_calls=len(result.tool_calls) if result else 0,
            context_keys=list(result.context_keys) if result else [],
            required_capabilities=list(task.required_capabilities),
        )
        edge(parent, task_node, "delegates")
        for dependency in task.dependencies:
            if f"task:{dependency}" in seen:
                edge(f"task:{dependency}", task_node, "depends_on")

    # --- review + synthesis ---------------------------------------------------
    for index, review in enumerate(run.reviews):
        panel = [r.strip() for r in review.reviewer.split(",") if r.strip()]
        label = (
            registry.get(panel[0]).name
            if len(panel) == 1 and panel[0] in registry
            else f"Review panel ({len(panel)})"
        )
        review_node = node(
            f"review:{index}",
            parent_id=root,
            kind="reviewer",
            agent=label,
            agent_id=review.reviewer,
            reviewers=panel,
            division="orchestration",
            task=review.summary[:200],
            status=getattr(review.verdict, "value", str(review.verdict)),
            spawned=True,
            findings=len(review.findings),
            iteration=index + 1,
        )
        for task in run.graph:
            if f"task:{task.id}" in seen and run.results.get(task.id):
                edge(f"task:{task.id}", review_node, "reviewed_by")
        edge(review_node, root, "reports_to")

    if run.final_output:
        synthesis = node(
            "synthesis",
            parent_id=root,
            kind="synthesis",
            agent=entry_def.name if entry_def else run.entry_agent,
            agent_id=run.entry_agent,
            division="orchestration",
            task="Final response",
            status=run.status.value,
            spawned=True,
        )
        edge(root, synthesis, "delegates")

    return {
        "run_id": run.id,
        "root_task": run.request,
        "status": run.status.value,
        "entry_agent": run.entry_agent,
        "requires_human_approval": run.requires_human_approval,
        "started_at": run.to_dict()["started_at"],
        "duration_s": round(run.duration_s, 3),
        "usage": run.usage.to_dict(),
        "budget": dict(run.budget),
        "nodes": nodes,
        "edges": edges,
        "counts": _counts(nodes),
    }


def _counts(nodes: list[dict]) -> dict:
    running = [n for n in nodes if n.get("status") == TaskStatus.RUNNING.value]
    return {
        "nodes": len(nodes),
        "spawned": sum(1 for n in nodes if n.get("spawned")),
        "completed": sum(1 for n in nodes if n.get("status") == TaskStatus.COMPLETED.value),
        "failed": sum(1 for n in nodes if n.get("status") == TaskStatus.FAILED.value),
        "running": len(running),
        "currently_running": [n["agent"] for n in running],
    }


# --- text rendering -----------------------------------------------------------

_STATUS_MARK = {
    TaskStatus.COMPLETED.value: "done",
    TaskStatus.FAILED.value: "FAILED",
    TaskStatus.RUNNING.value: "running",
    TaskStatus.SKIPPED.value: "skipped",
    TaskStatus.CANCELLED.value: "cancelled",
}


def render_tree(agent_map: dict, *, width: int = 100) -> str:
    """Draw the Agent Map as an indented tree for the terminal."""
    children: dict[str | None, list[dict]] = {}
    for node in agent_map["nodes"]:
        children.setdefault(node.get("parent_id"), []).append(node)

    lines: list[str] = []

    def walk(node: dict, prefix: str, last: bool) -> None:
        connector = "" if prefix == "" and node.get("parent_id") is None else (
            "`-- " if last else "|-- "
        )
        status = _STATUS_MARK.get(node.get("status", ""), node.get("status", ""))
        duration = f" {node['duration_s']:.1f}s" if node.get("duration_s") else ""
        label = f"{prefix}{connector}{node['agent']}"
        detail = f"[{status}{duration}]"
        pad = max(1, width - len(label) - len(detail))
        lines.append(f"{label}{' ' * pad}{detail}")

        task = (node.get("task") or "").strip().replace("\n", " ")
        if task:
            child_prefix = prefix + ("    " if last else "|   ") if connector else prefix
            lines.append(f"{child_prefix}    {task[:width - len(child_prefix) - 6]}")

        kids = children.get(node["id"], [])
        child_prefix = prefix + ("    " if last else "|   ") if connector else prefix
        for index, child in enumerate(kids):
            walk(child, child_prefix, index == len(kids) - 1)

    roots = children.get(None, [])
    for index, node in enumerate(roots):
        walk(node, "", index == len(roots) - 1)
    return "\n".join(lines)
