# The Runtime

Everything else in this folder is a **specification** — what the kernel is supposed to do. This page
points at the code that does it: [`runtime/`](../../runtime/README.md), a dependency-free Python
package that reads the [agent specs](../agents/README.md) and actually executes them.

```bash
python -m companyos run "Design and implement authentication for a web application."
```

## Definition vs. Instance

This is the distinction the runtime is built around, and the reason there are not 107 agents running.

| | **Agent Definition** | **Agent Instance** |
|---|---|---|
| Means | "What this *type* of agent is" | "A temporary agent handling *one* task" |
| Lives in | `ai/agents/**/*.md` — this repository | Memory, for the length of one task |
| How many | 117 (107 specs + the kernel agents here) | Usually 3–6 per run; hard-capped |
| Lifetime | Permanent, version-controlled | Spawned, executes, result captured, terminated |
| Changed by | Editing the Markdown | Nothing — it is immutable input plus one task |

An agent spec is a **template**. A run instantiates only the agents its task calls for.

## How the specs drive the code

| This specification | Is executed by |
|---|---|
| [ceo-agent.md](ceo-agent.md) | the entry agent and the synthesizer |
| [planner.md](planner.md) | `orchestration/planner.py` |
| [task-decomposer.md](task-decomposer.md) | `orchestration/decomposer.py` |
| [coordinator.md](coordinator.md) · [task-routing.md](task-routing.md) | `orchestration/selector.py` + `orchestration/scheduler.py` |
| [reviewer.md](reviewer.md) · [qa-reviewer.md](qa-reviewer.md) · [security-reviewer.md](security-reviewer.md) · [documentation-reviewer.md](documentation-reviewer.md) | `orchestration/reviewer.py` |
| [approval-engine.md](approval-engine.md) | the `AWAITING_APPROVAL` run state; a Security Reviewer block is never auto-cleared |
| [execution-lifecycle.md](execution-lifecycle.md) | `TaskStatus`, retry logic, and dependency-failure handling |
| [memory-manager.md](memory-manager.md) · [retrieval](../memory/retrieval.md) · [context](../memory/context-management.md) | the `memory/` package and the context builder |
| every file in [agents/](../agents/README.md) | the Agent Registry |

The runtime reads these files; it never rewrites them. Editing a spec changes how the agent behaves
on the next run.

## What the code adds

Things a specification cannot state, which only an implementation can provide:

- **Capability matching** — each spec is tagged from its own text, so selection is scored rather than
  routed through a hardcoded table.
- **Concurrency** — independent subtasks execute in parallel; dependent ones cannot.
- **Safeguards** — caps on spawned agents, task depth, review iterations, timeouts, and tokens.
- **Tool boundaries** — spawned agents get no shell, no network, and no filesystem writes.
- **The Agent Map** — the live execution graph, as data a UI can render.
- **Provider independence** — Anthropic, OpenAI, local models, or an offline mock.

## Where to go next

- [runtime/README.md](../../runtime/README.md) — how it works and how to run it
- [runtime/docs/architecture-assessment.md](../../runtime/docs/architecture-assessment.md) — why it is shaped this way
- [agents/agent-template.md](../agents/agent-template.md) — add an agent; the runtime discovers it with no code change
