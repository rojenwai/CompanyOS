# CompanyOS Runtime

**The executable form of the [orchestration kernel](../ai/orchestration/README.md).**

`ai/agents/` holds 107 agent *specifications*. This package reads them and runs them: it selects the
agents a request needs, spawns temporary instances of them, executes independent work in parallel,
reviews the results, and synthesizes an answer.

No dependencies. No API key required to try it.

```bash
python -m companyos run "Design and implement authentication for a web application."
```

---

## The distinction everything rests on

| | Agent **Definition** | Agent **Instance** |
|---|---|---|
| **What it is** | "What this *type* of agent is" | "A temporary agent handling *one* task" |
| **Lives in** | `ai/agents/**/*.md` — Markdown, version-controlled | Memory, for the duration of one task |
| **Count** | 117 (107 specs + the kernel agents) | Typically 3–6 per run, capped by `max_agents` |
| **Lifetime** | Forever | Spawned → executes → result captured → terminated |
| **State** | Immutable, shared | Its own task, scoped context, and tool grant |
| **Type** | [`AgentDefinition`](companyos/registry/definition.py) | [`AgentInstance`](companyos/orchestration/spawner.py) |

**There are never 107 running agents.** The registry holds 117 definitions; a run instantiates only
the handful the task actually calls for, and terminates each one as soon as its result is captured.

---

## The flow

```
User request
    │
    ▼
CEO / entry agent ──────────── receives the request, owns the final answer
    │
    ▼
Planner ────────────────────── objective + required capabilities   (ai/orchestration/planner.md)
    │
    ▼
Task Decomposer ────────────── subtask DAG                  (ai/orchestration/task-decomposer.md)
    │
    ▼
Agent Selection ────────────── capability matching against the registry
    │
    ▼
Dynamic Spawning ───────────── one temporary instance per task
    ├── Agent A ──┐
    ├── Agent B ──┤ parallel where independent, sequential where dependent
    └── Agent C ──┘
    │
    ▼
Result Aggregation ─────────── successes, failures, partials, metadata
    │
    ▼
Reviewer panel ─────────────── Reviewer · QA · Security · Documentation
    │                             │
    │                             └── revise → back to the author, with findings
    ▼
Synthesis ──────────────────── the entry agent composes the final answer
    │
    ▼
Final response + Agent Map
```

---

## Components

| Component | Module | Reads its behaviour from |
|---|---|---|
| **Agent Registry** | [`registry/registry.py`](companyos/registry/registry.py) | `ai/agents/**`, `ai/orchestration/*` |
| Spec parser | [`registry/parser.py`](companyos/registry/parser.py) | the 11-section spec format |
| Capability taxonomy | [`registry/capabilities.py`](companyos/registry/capabilities.py) | — |
| **Planner** | [`orchestration/planner.py`](companyos/orchestration/planner.py) | [`planner.md`](../ai/orchestration/planner.md) |
| **Task Decomposer** | [`orchestration/decomposer.py`](companyos/orchestration/decomposer.py) | [`task-decomposer.md`](../ai/orchestration/task-decomposer.md) |
| **Agent Selector** | [`orchestration/selector.py`](companyos/orchestration/selector.py) | [`task-routing.md`](../ai/orchestration/task-routing.md) |
| **Agent Spawner** | [`orchestration/spawner.py`](companyos/orchestration/spawner.py) | — |
| **Scheduler** | [`orchestration/scheduler.py`](companyos/orchestration/scheduler.py) | [`coordinator.md`](../ai/orchestration/coordinator.md) |
| **Context builder** | [`orchestration/context.py`](companyos/orchestration/context.py) | [`context-management.md`](../ai/memory/context-management.md) |
| **Result Aggregator** | [`orchestration/aggregator.py`](companyos/orchestration/aggregator.py) | — |
| **Reviewer** | [`orchestration/reviewer.py`](companyos/orchestration/reviewer.py) | [`reviewer.md`](../ai/orchestration/reviewer.md), [`approval-engine.md`](../ai/orchestration/approval-engine.md) |
| **Synthesizer** | [`orchestration/synthesizer.py`](companyos/orchestration/synthesizer.py) | [`ceo-agent.md`](../ai/orchestration/ceo-agent.md) |
| **Agent Map** | [`orchestration/agent_map.py`](companyos/orchestration/agent_map.py) | — |
| **Memory** | [`memory/`](companyos/memory/) | [`ai/memory/`](../ai/memory/README.md), [`retrieval.md`](../ai/memory/retrieval.md) |
| **Tools + policy** | [`tools/`](companyos/tools/) | each spec's section 5 |
| **Providers** | [`providers/`](companyos/providers/) | — |
| **Observability** | [`observability/trace.py`](companyos/observability/trace.py) | [`execution-lifecycle.md`](../ai/orchestration/execution-lifecycle.md) |

---

## Agent selection

Selection is capability-driven. There is no `if task == X: use agent Y` table anywhere.

Each definition is tagged at load time by matching a **capability taxonomy** against its own spec
text, title and folder. A task's required capabilities are then scored against every definition:

| Signal | Weight | Why |
|---|---|---|
| Exact capability match | ×3.0, amplified by depth | The agent's spec claims this capability |
| Capability **depth** | +0.25 per extra signal phrase | The Database Engineer mentions databases five times; the API Architect once |
| Named for the capability | +1.0 | "Database Engineer" *is* the database agent |
| Same namespace | ×1.25 | `security.pentest` still points at the security division |
| Lexical fit (IDF) | ×2.0 | Catches wording the taxonomy has no phrase for |
| Owning division | +0.75 | Structural prior |
| Delegator | **excluded** | An executive delegates; it never owns a deliverable |

Inspect it directly:

```bash
python -m companyos select "threat model the login flow" -c security.threat-modeling
```

```
  score  agent                                                matched capabilities
   6.50  security/security-architect-agent                    security.threat-modeling
   4.25  security/penetration-testing-agent                   security.threat-modeling
   2.50  security/compliance-privacy-agent                    security.threat-modeling
```

**Adding an agent requires no code.** Drop a new 11-section Markdown spec into
`ai/agents/<division>/`; it is discovered, tagged, and selectable on the next run.

---

## Parallel execution

The [scheduler](companyos/orchestration/scheduler.py) walks the task DAG and starts a task the moment
*its own* dependencies complete — it does not wait for a whole wave. Independent tasks run
concurrently up to `max_parallel`; dependent ones cannot overlap by construction.

```
Task A ──┐                         Research
Task B ──┼──→ aggregator              ↓
Task C ──┘                         Analysis
                                      ↓
   concurrent                    Recommendation
                                   sequential
```

A failed task marks only its own dependents `SKIPPED`. The rest of the run continues, and the gap is
stated in the final answer rather than hidden. A dependency marked `optional` does not block its
dependents when it fails.

---

## The reviewer loop

After aggregation, the reviewer agents whose concerns the work raises run **in parallel** over the
combined results. Their verdicts merge worst-first:

```
approve → approve_with_changes → revise → reject → escalate → block
```

- **revise / reject** → the affected tasks go back *to their original author* with the findings
  attached (a deterministic failure returns to the author, per
  [`execution-lifecycle.md`](../ai/orchestration/execution-lifecycle.md) — never a blind retry).
  Bounded by `max_iterations` and `max_attempts_per_task`.
- **escalate** → the run finishes but is flagged for a human.
- **block** → only the Security Reviewer can issue one. It sets the run to `AWAITING_APPROVAL` and is
  never auto-cleared ([`approval-engine.md`](../ai/orchestration/approval-engine.md)).

A reviewer that *fails to run* escalates. It never silently approves.

---

## Context isolation

Each instance receives its own task, the parent objective, **the outputs of the tasks it actually
depends on**, its own reviewer findings, and a bounded memory retrieval. It does not receive the
conversation, sibling branches, or peers' outputs.

Everything an agent did not write itself is wrapped:

```
<untrusted source="agent:research/market-research-agent">
...another agent's output...
</untrusted>
```

and every system prompt declares that such blocks are **data, not instructions**. `AgentResult.context_keys`
records exactly which slices an instance was given, so isolation is auditable after the fact.

---

## Safeguards

| Limit | Default | Stops |
|---|---|---|
| `max_agents` | 12 | Runaway spawning |
| `max_depth` | 3 | Unbounded nesting |
| `max_iterations` | 2 | Endless plan/review cycles |
| `max_parallel` | 4 | Resource exhaustion |
| `max_attempts_per_task` | 2 | Retry loops |
| `task_timeout_s` | 120 | A hung agent |
| `run_timeout_s` | 600 | A hung run |
| `max_total_tokens` | 400 000 | Cost |
| `max_tool_calls_per_agent` | 8 | Tool loops |
| `max_context_chars` | 24 000 | Context bloat |

Every one is enforced in code and covered by a test. Hitting one degrades the run — it finishes with
what it has and says so — rather than crashing.

---

## Security model

Spawned agents act on model-generated instructions, so they are treated as untrusted:

- **No shell, no network, no filesystem writes.** Those tools exist only as explicit refusals.
- **Default-deny tools.** A grant must survive the runtime denylist, the spec's own prohibitions, and
  a mutating-tool check. A spawned agent always has strictly less authority than the process running it.
- **Path sandbox.** Reads are confined to `ai/`, `handbook/`, `starter-kits/`; absolute paths, rooted
  paths, traversal, and non-text files are refused.
- **No secrets reach agents.** API keys live in the provider layer; `ToolContext` carries no
  environment and no provider handle.
- **Memory writes are proposals.** No temporary instance writes persistent organizational memory;
  promotion is a separate, policy-gated step (off by default).

---

## Providers

The orchestrator talks to one interface and never to a vendor SDK.

| Name | Backend |
|---|---|
| `mock` | Offline, deterministic. The default. |
| `anthropic` | Messages API (`ANTHROPIC_API_KEY`) |
| `openai` | Chat Completions (`OPENAI_API_KEY`) |
| `local` | Any OpenAI-compatible server — Ollama, vLLM, LM Studio — via `--base-url` |

```bash
python -m companyos run "..." --provider anthropic --model claude-sonnet-5
python -m companyos run "..." --provider local --base-url http://localhost:11434/v1
```

Register your own with `companyos.providers.register_provider(name, factory)`.

### About the mock provider

`mock` is a real provider with a rule-based stand-in for a model, so an offline run exercises the
**actual** orchestration path — real registry, real capability matching, real DAG scheduling, real
reviewer loop. Its prose output is labelled `[simulated output]`. It is for exercising the machinery
and for tests; it is not a substitute for a model's reasoning.

---

## Running it

```bash
python -m companyos doctor                     # check specs, memory, and paths
python -m companyos run "<request>"            # orchestrate, offline
python -m companyos run "<request>" -v         # stream every event
python -m companyos run "<request>" --map m.json --save run.json
python -m companyos agents list --division security
python -m companyos agents show cto-agent
python -m companyos select "<task>" -c <capability>
python -m companyos capabilities
python -m companyos map m.json                 # render a saved Agent Map
```

From Python:

```python
from companyos import Orchestrator, RuntimeConfig

config = RuntimeConfig.load()                  # auto-detects the repo root
orchestrator = Orchestrator(config)
run = orchestrator.run_sync("Design and implement authentication.")

print(run.final_output)
print(orchestrator.agent_map(run))             # the execution graph, as data
```

Configuration can also come from a `companyos.json` at the repository root:

```json
{
  "provider": { "name": "anthropic", "model": "claude-sonnet-5" },
  "limits":   { "max_agents": 8, "max_parallel": 3 },
  "denied_tools": ["shell", "write_file", "http_request", "remember"]
}
```

---

## Agent Map

Every run produces a serializable execution graph — the data a UI renders. It is a pure projection of
the run record, so it can be rebuilt at any time from a saved run.

```json
{
  "run_id": "run_a97b09b5",
  "root_task": "Design and implement authentication for a web application.",
  "status": "completed",
  "nodes": [
    { "id": "entry", "parent_id": null, "kind": "entry", "agent": "CEO Agent", "status": "completed" },
    { "id": "supervisor:executive/chief-security-officer-agent", "parent_id": "decomposer",
      "kind": "supervisor", "agent": "Chief Security Officer Agent", "spawned": false,
      "status": "delegated" },
    { "id": "task:task_3f9a", "parent_id": "supervisor:executive/chief-security-officer-agent",
      "kind": "agent", "agent": "Security Architect Agent", "status": "completed",
      "spec_state": "DONE", "spawned": true, "duration_s": 0.004,
      "usage": { "total_tokens": 812 }, "context_keys": ["your task", "why this work exists"] }
  ],
  "edges": [
    { "from": "decomposer", "to": "supervisor:executive/chief-security-officer-agent", "type": "delegates" },
    { "from": "task:task_1", "to": "task:task_4", "type": "depends_on" }
  ],
  "counts": { "nodes": 11, "spawned": 5, "completed": 5, "failed": 0, "currently_running": [] }
}
```

Node kinds: `entry`, `kernel`, `supervisor`, `agent`, `reviewer`, `synthesis`.
Edge types: `delegates`, `depends_on`, `reviewed_by`, `reports_to`.

`supervisor` nodes carry `spawned: false`. They are the chain of accountability drawn from the specs'
own reporting lines — the CTO is shown as owning engineering work **without an instance of the CTO
being created**.

`render_tree()` draws the same document for a terminal.

---

## Observability

Every run writes a JSONL trace to `.companyos/runs/<run_id>.jsonl`, one line per event:

```
run.started · plan.created · tasks.decomposed · agent.selected · agent.spawned · agent.started
agent.completed | agent.failed | agent.timeout · agent.terminated · tool.called | tool.denied
task.status · task.skipped · task.retry · review.started · review.completed · approval.required
memory.proposed · limit.exceeded · synthesis.started · run.completed
```

Each carries the run id, task id, agent id, parent agent, timestamp, and step-specific data.

---

## Tests

220 tests, stdlib `unittest`, no network and no API keys — the mock provider stands in for the model.

```bash
python runtime/run_tests.py          # from the repo root
python -m unittest discover -s tests # from runtime/
pytest tests                         # if you have pytest
```

| File | Covers |
|---|---|
| [`test_registry.py`](tests/test_registry.py) | Discovery, both header dialects, capability extraction, hierarchy, a new spec becoming selectable |
| [`test_selector.py`](tests/test_selector.py) | Per-capability selection, depth weighting, delegator exclusion, team selection, reviewer selection |
| [`test_decomposer.py`](tests/test_decomposer.py) | Planning, decomposition, and hostile model output — cycles, duplicate ids, forward refs, junk |
| [`test_graph.py`](tests/test_graph.py) | DAG validation, topological order, waves, readiness, optional dependencies |
| [`test_scheduler.py`](tests/test_scheduler.py) | Real concurrency, enforced sequencing, dependency failure, timeouts, cancellation |
| [`test_spawner.py`](tests/test_spawner.py) | Instance lifecycle, tool grants, `max_agents`, `max_depth`, tool-call budget |
| [`test_tools.py`](tests/test_tools.py) | Sandbox escapes, permission denial, refused tools, memory proposals |
| [`test_context.py`](tests/test_context.py) | Context isolation, untrusted wrapping, truncation, findings injection |
| [`test_reviewer.py`](tests/test_reviewer.py) | Verdict merging, the security block, reviewer failure, aggregation |
| [`test_memory.py`](tests/test_memory.py) | Retrieval contract, "no reliable source", promotion gating, scratchpad scoping |
| [`test_orchestrator.py`](tests/test_orchestrator.py) | End-to-end runs, parallelism, the review loop, failure handling, budgets, cancellation |
| [`test_agent_map.py`](tests/test_agent_map.py) | Map shape, hierarchy, metadata, pure projection, failure visibility |
| [`test_providers.py`](tests/test_providers.py) | Provider resolution, preflight, Anthropic and OpenAI wire formats, JSON extraction |
| [`test_config.py`](tests/test_config.py) | Root discovery, limit validation, budget counters, config files |

---

## Extending it

- **Add an agent** — write the Markdown spec. Nothing else.
- **Add a capability** — one entry in `TAXONOMY` ([`capabilities.py`](companyos/registry/capabilities.py)).
- **Add a provider** — implement `Provider.complete`, call `register_provider`.
- **Add a tool** — define a `Tool`, add it to `BUILTIN_TOOLS`, grant it via `default_tools`.
- **Distribute it** — `DAGScheduler` is the only component that assumes local execution. Replacing its
  `execute` callable with a queue producer is the seam for workers and distributed runs.

See [docs/architecture-assessment.md](docs/architecture-assessment.md) for the pre-implementation
survey of what existed and why the runtime is shaped this way.
