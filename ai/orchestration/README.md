# Orchestration — The Kernel

Orchestration is how Company OS turns a request into coordinated, reviewed, approved, and executed
work across a workforce of specialized [agents](../agents/README.md). No agent works alone on major
decisions; the kernel is what makes many narrow experts behave like one reliable organization.

> **This kernel is executable.** The pages below specify the behaviour; [runtime.md](runtime.md)
> points at the code that performs it — selecting agents for a request, spawning temporary instances
> of them, running independent work in parallel, reviewing it, and synthesizing the result.
> Run it with `python -m companyos run "<your request>"`.

---

## The orchestration model

```
Request
  │
  ▼
CEO Agent ──────────────► sets objective, delegates
  │
  ▼
Planner ────────────────► breaks work into a plan
  │
  ▼
Task Decomposer ────────► subtasks + dependencies
  │
  ▼
Coordinator ────────────► routes subtasks to specialist agents (see task-routing.md)
  │        ▲
  │        │ context from Memory Manager + Knowledge Manager
  ▼        │
Specialist Agents ──────► produce deliverables
  │
  ▼
Reviewers (Reviewer · QA · Security · Documentation)
  │
  ▼
Approval Engine ────────► gates + Human-in-the-Loop where required
  │
  ▼
Execution Engine ───────► executes/ships, enforces quality gates
  │
  ▼
Continuous Improvement Engine ──► captures lessons → Memory
```

## Components

### Coordination agents (full specs)
| Component | Role |
|---|---|
| [ceo-agent.md](ceo-agent.md) | Orchestrates everything; delegates, never implements |
| [planner.md](planner.md) | Turns objectives into execution plans |
| [task-decomposer.md](task-decomposer.md) | Splits plans into subtasks with dependencies |
| [coordinator.md](coordinator.md) | Routes and schedules work across agents |
| [memory-manager.md](memory-manager.md) | Supplies and updates [memory](../memory/) |
| [knowledge-manager.md](knowledge-manager.md) | Supplies retrieved [knowledge](../memory/knowledge-base.md) |
| [reviewer.md](reviewer.md) | General correctness/quality review |
| [qa-reviewer.md](qa-reviewer.md) | Test and quality review |
| [security-reviewer.md](security-reviewer.md) | Security review |
| [documentation-reviewer.md](documentation-reviewer.md) | Documentation review |

### Engines & processes
| Component | Role |
|---|---|
| [approval-engine.md](approval-engine.md) | Applies gates and Human-in-the-Loop approvals |
| [execution-engine.md](execution-engine.md) | Executes approved work; enforces quality gates |
| [continuous-improvement-engine.md](continuous-improvement-engine.md) | Turns outcomes into lessons |
| [task-routing.md](task-routing.md) | How subtasks map to agents |
| [execution-lifecycle.md](execution-lifecycle.md) | Delegation, conflict resolution, retry logic, lifecycle states |
| [runtime.md](runtime.md) | The executable kernel: agent **definitions** vs. running **instances** |

The engines enforce [governance](../../handbook/governance/): the [decision framework](../../handbook/governance/decision-framework.md),
[quality gates](../../handbook/governance/quality-gates.md), and [definition of done](../../handbook/governance/definition-of-done.md).
