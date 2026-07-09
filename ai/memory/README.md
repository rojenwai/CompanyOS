# Memory

Memory is the persistent, structured knowledge that lets Company OS improve over time instead of
relearning everything each session. The [Memory Manager](../orchestration/memory-manager.md) and
[Knowledge Manager](../orchestration/knowledge-manager.md) own reads and writes; memory is **never
modified without validation**.

## Memory types

| Store | Scope | File |
|---|---|---|
| Session | Current conversation only | [session-memory.md](session-memory.md) |
| Project | One project's architecture, requirements, decisions | [project-memory.md](project-memory.md) |
| Company | Standards, principles, conventions, policies | [company-memory.md](company-memory.md) |
| Department | A department's operating knowledge | [department-memory.md](department-memory.md) |
| User | Preferences, goals, constraints, prior work | [user-memory.md](user-memory.md) |
| Customer | Customer context and history | [customer-memory.md](customer-memory.md) |
| Research | Findings, benchmarks, sources | [research-memory.md](research-memory.md) |
| Architecture | System designs and their rationale | [architecture-memory.md](architecture-memory.md) |
| Decision | Decisions and why they were made | [decision-memory.md](decision-memory.md) |
| Meeting | Meeting decisions and action items | [meeting-memory.md](meeting-memory.md) |
| Documentation | Canonical docs index | [documentation-memory.md](documentation-memory.md) |
| Lessons Learned | What worked, what failed | [lessons-learned.md](lessons-learned.md) |
| Prompt | Reusable, versioned prompts | [prompt-memory.md](prompt-memory.md) |
| Knowledge Base | Concepts, algorithms, references | [knowledge-base.md](knowledge-base.md) |

## Cross-cutting mechanics

| Concern | File |
|---|---|
| How context is assembled and bounded | [context-management.md](context-management.md) |
| How memory is retrieved | [retrieval.md](retrieval.md) |
| Updates, retention, and versioning | [retention-and-versioning.md](retention-and-versioning.md) |

## Principles

- **Validated writes only** — no hallucinated memory; every fact has a source and timestamp.
- **Right memory, right scope** — session facts never leak into company memory without promotion.
- **Retrievable** — everything is tagged for [retrieval](retrieval.md).
- **Versioned** — memory changes are traceable and reversible.
