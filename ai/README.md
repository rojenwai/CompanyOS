# AI — the machine side

**Everything the AI agent workforce runs on.** This is not reading material about AI; it is the
operational specification of the agents themselves, how they are coordinated, and what they remember.

The human side lives in [handbook/](../handbook/README.md). Note the distinction:

- **`ai/`** (here) — the AI *workforce*: who the agents are, how work is routed, reviewed, approved, and remembered.
- **[handbook/departments/ai-engineering/](../handbook/departments/ai-engineering/README.md)** — the *discipline* of building AI products (RAG, evaluation, prompt standards, AI security). That's reading material.

## Index

| Area | What's inside | Customize? |
|---|---|---|
| [agents/](agents/README.md) | The registry of **93 agent specs**, one folder per department, all following the [standard 11-section spec](agents/agent-template.md) | ✏️ **Always** — activate/remove/add agents |
| [orchestration/](orchestration/README.md) | The kernel — [CEO agent](orchestration/ceo-agent.md) · [planner](orchestration/planner.md) · [task decomposer](orchestration/task-decomposer.md) · [coordinator](orchestration/coordinator.md) · [reviewers](orchestration/reviewer.md) · [approval](orchestration/approval-engine.md)/[execution](orchestration/execution-engine.md)/[improvement](orchestration/continuous-improvement-engine.md) engines · [lifecycle](orchestration/execution-lifecycle.md) | ⚙️ Sometimes |
| [memory/](memory/README.md) | 14 memory types (session, project, company, customer, decision, [lessons-learned](memory/lessons-learned.md), [prompt](memory/prompt-memory.md), [knowledge-base](memory/knowledge-base.md)…) + [retrieval](memory/retrieval.md) · [retention & versioning](memory/retention-and-versioning.md) | ⚙️ Sometimes |

## How it connects to the handbook

Every department in [handbook/departments/](../handbook/departments/README.md) has a matching agent folder
here (`ai/agents/<department>/`). The department's `agents.md` indexes them; the agents enforce that
department's [standards](../handbook/standards/README.md) and pass its
[quality gates](../handbook/governance/quality-gates.md).

## Customizing

- **Activate only the agents you need.** Delete the rest — they are specs, not code.
- **Add an agent:** copy [agents/agent-template.md](agents/agent-template.md) and fill in all 11 sections.
- **Keep the kernel.** `orchestration/` and `memory/` are the framework; change them only if you are
  changing how work is routed or remembered.

See [CUSTOMIZE.md](../CUSTOMIZE.md).
