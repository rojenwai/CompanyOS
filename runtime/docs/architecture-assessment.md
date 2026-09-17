# Architecture assessment

Written before the runtime was implemented, recording what CompanyOS was at that point and why the
runtime is shaped the way it is. Kept as the rationale behind the design, not as current-state docs —
for those, see [the runtime README](../README.md).

---

## What existed

849 Markdown files and 4 Python documentation-lint scripts. **No runtime code.** Every component the
runtime needed to "extend" existed only as prose.

| Concern | What was there | Form |
|---|---|---|
| Orchestration kernel | [`ai/orchestration/README.md`](../../ai/orchestration/README.md) — a flow diagram | specification |
| Planner | [`planner.md`](../../ai/orchestration/planner.md) — an 11-section agent spec | specification |
| Task decomposer | [`task-decomposer.md`](../../ai/orchestration/task-decomposer.md) | specification |
| Coordinator / routing | [`coordinator.md`](../../ai/orchestration/coordinator.md), [`task-routing.md`](../../ai/orchestration/task-routing.md) | specification |
| Execution lifecycle | [`execution-lifecycle.md`](../../ai/orchestration/execution-lifecycle.md) — states, retries, conflicts | specification |
| Reviewers | Reviewer, QA, Security, Documentation | specification |
| Approval / HITL | [`approval-engine.md`](../../ai/orchestration/approval-engine.md) | specification |
| Agent definitions | **107 specs**, all in one fixed 11-section shape | specification — *the real asset* |
| Memory | 14 typed stores + [retrieval](../../ai/memory/retrieval.md) and [context](../../ai/memory/context-management.md) contracts | specification |
| LLM provider abstraction | none | — |
| API / CLI / entry point | none | — |
| Tests | none (doc lint only) | — |

## What that implied

**1. The work is additive, not a rewrite.** Nothing needed modifying in the dangerous sense. The 107
specs became the registry's source of truth, parsed at load and never duplicated. The only existing
files touched were index and documentation pages.

**2. The specs are unusually good input.** Every spec has the same 11 sections, a declared division
and reporting line, and a tools section. That regularity is what makes a generic parser and a
capability taxonomy viable instead of per-agent configuration.

**3. The spec vocabulary was reused rather than replaced.** `execution-lifecycle.md` already defines
`QUEUED → ASSIGNED → IN_PROGRESS → IN_REVIEW → AWAITING_APPROVAL → EXECUTING → DONE`. `TaskStatus` is
that lifecycle plus the states a real scheduler needs (`SKIPPED`, `CANCELLED`, `RETRYING`), and
[`spec_state()`](../companyos/status.py) maps back onto the documented names so dashboards and the
handbook stay consistent. Reviewer verdicts, the Security Reviewer's non-overridable block, and the
"return to author with findings, never blind-retry" rule are likewise enforced in code because the
specs already state them.

**4. CI constrained where the code could live.** [`docs-check.yml`](../../.github/workflows/docs-check.yml)
requires that every relative link resolves, that no `.md` under `ai/` or `handbook/` contains
placeholder text, tabs or trailing whitespace, and that **every `.md` under `ai/agents/` has exactly
11 numbered sections**. Putting a Python package inside `ai/` would have forced a `README.md` into
every subpackage and risked tripping the section checker. Hence a new top-level `runtime/`.

**5. Zero dependencies was achievable, so it was required.** The environment had Python 3.13 with no
pytest and no PyYAML. Providers are implemented over `urllib`, and tests over `unittest`, so the
runtime clones and runs with nothing installed — which matters for a repository whose point is that
you clone it and make it yours.

## Design consequences

| Decision | Because |
|---|---|
| Registry parses Markdown; never copies it | The specs stay the single source of truth, editable by non-programmers |
| Capabilities extracted from spec text, title and folder | A new spec becomes selectable with no code change |
| Selection scored, never tabulated | The brief explicitly ruled out `if task == X: use agent Y` |
| Delegators hard-excluded from executable work | The specs say executives delegate and do not implement |
| Supervisor nodes in the Agent Map are not instances | Shows accountability without spawning 14 executives |
| Two-phase memory writes | `memory-manager.md`: "never writes unvalidated memory" |
| Default-deny tools, no shell or network | Spawned agents act on model-generated instructions |
| `purpose` metadata on provider calls | Lets the mock provider serve every orchestration step without the orchestrator knowing which provider it has |

## Known limits of this shape

- **Single process.** `DAGScheduler` assumes local `asyncio`. Its `execute` callable is the seam where
  a queue or worker pool would be substituted.
- **The taxonomy is hand-written.** ~90 capabilities with keyword signals. It covers the 20 divisions
  present, and a request using vocabulary nothing matches falls back to lexical scoring, but it is
  curated, not learned.
- **No embeddings.** Retrieval and lexical scoring are IDF over tokens. Sufficient for 117 specs and
  17 memory documents; a larger corpus would want vectors.
- **Agents do not spawn agents.** Hierarchy is expressed through the task DAG and the delegation
  chain, not by an agent calling the spawner — which is deliberate, since uncontrolled recursive
  spawning is exactly what `max_agents` and `max_depth` exist to prevent.
