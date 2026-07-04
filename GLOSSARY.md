# Company OS — Glossary

Shared vocabulary for the whole repository. Use these terms consistently.

| Term | Definition |
|---|---|
| **Company OS** | This repository: the operating system for an AI-native company. |
| **Department** | A self-contained functional area (engineering, product, finance…) that follows the [standard department structure](STRUCTURE.md#standard-department-structure). |
| **Kernel** | The core coordination layer: [orchestration](orchestration/), [memory](memory/), and [agents](agents/). Everything else plugs into it. |
| **Agent** | A specialized AI worker defined by the [standard agent spec](agents/agent-template.md). Agents never work alone on major decisions. |
| **CEO Agent** | The top-level orchestrator. Delegates and reviews; never performs specialist implementation. |
| **Division** | A grouping of agents by function (Research, Product, Engineering, AI, Hardware, …). |
| **Orchestration** | How tasks are routed, delegated, reviewed, approved, and executed across agents. |
| **Memory** | Persistent structured knowledge across sessions: company, project, customer, research, decision, and knowledge memory. |
| **Quality Gate** | A checkpoint that work must pass before it can progress to the next phase. |
| **Definition of Ready (DoR)** | The conditions a task must meet before work starts. |
| **Definition of Done (DoD)** | The conditions a task must meet to be considered complete (production-ready, not merely implemented). |
| **SDLC** | The 20-phase [Software Development Lifecycle](workflows/sdlc.md) every project follows. |
| **Playbook** | A situational, step-by-step guide for a recurring scenario (launch, incident, breach…). |
| **SOP** | Standard Operating Procedure — the routine, repeatable way a task is done. |
| **PRD** | Product Requirements Document. |
| **RFC** | Request for Comments — a proposal document for a significant change. |
| **ADR** | Architecture Decision Record — a captured, dated architectural decision. |
| **Starter Kit** | A preconfigured company type that inherits core Company OS and adds domain-specific practice. |
| **Seeded** | A department populated with real migrated content but not yet expanded to the full structure. |
| **North Star Metric** | The single metric that best captures the value a product delivers to customers. |
| **PMF** | Product-Market Fit. |
| **TAM / SAM / SOM** | Total / Serviceable Available / Serviceable Obtainable Market. |
| **DoR / DoD** | See Definition of Ready / Definition of Done above. |
| **EOL** | End-of-Life — the managed retirement of a product or version. |
| **Human-in-the-Loop (HITL)** | A required human approval step for high-risk or irreversible actions. |
| **RAG** | Retrieval-Augmented Generation — retrieve authoritative context before generating. |
