# Company OS — Structure & Authoring Conventions

This document defines how Company OS is organized and how every file in it is written. It is the
contract that makes the system predictable: once you know the pattern, you can navigate or extend
any part of the repository.

---

## Top-level layout

```
company-os (repository root)
│
├── company/              Identity: mission, vision, principles, structure, roles
├── governance/           Decision rights, quality gates, communication, definition of done
│
├── orchestration/        The kernel: CEO agent, planner, engines, execution lifecycle
├── memory/               Memory architecture: types, retrieval, retention, versioning
├── agents/               AI agent registry + the standard agent specification
│
│                         20 departments, all full (18 files + templates/ checklists/ examples/):
├── engineering/  product/  post-launch/  design/  research/  ai/  strategy/
├── security/  devops/  finance/  legal/  hr/  operations/  marketing/
├── sales/  customer-success/  data/  documentation/  hardware/  investor-relations/
│
├── workflows/            Cross-department processes (e.g. the SDLC)
├── standards/            Company-wide standards
├── playbooks/            Operational playbooks
├── templates/            Reusable department + document templates
├── starter-kits/         Preconfigured company types that inherit core Company OS
│
├── docs/                 Cross-cutting guides (Company-Building Guide, ROADMAP)
├── scripts/              Repo tooling (e.g. link checker)
├── .github/              Community health files + CI workflows
│
├── README.md             The Company OS hub
├── STRUCTURE.md          This file
├── CONTRIBUTING.md       Authoring conventions
└── GLOSSARY.md           Shared vocabulary
```

The repository root **is** Company OS — there is no redundant `company-os/` nesting.

---

## Standard department structure

Every department is a miniature operating manual. It uses **exactly** this shape so that
engineering, finance, research, and legal all feel the same:

```
<department>/
├── README.md              Overview + index of the department
├── mission.md             Why this department exists
├── vision.md              Where it is going
├── principles.md          Non-negotiable operating principles
├── organization.md        Structure, reporting lines, interfaces
├── roles.md               Human + AI roles and their accountabilities
├── agents.md              Which AI agents operate here (links to agents/<dept>/)
├── workflows.md           Core repeatable processes
├── playbooks.md           Situational step-by-step guides
├── sops.md                Standard operating procedures
├── decision-frameworks.md How decisions are made here
├── standards.md           Department-specific standards
├── review-process.md      How work is reviewed
├── quality-gates.md       What must pass before work progresses
├── automation.md          What is automated and how
├── metrics.md             What is measured
├── dashboards.md          How metrics are surfaced
├── tools.md               Tooling used
├── templates/             Reusable templates for this department
├── checklists/            Reusable checklists
└── examples/              Worked examples
```

A **"seeded"** department has a real `README.md` plus the natural content files carrying its
migrated content; it is upgraded to the full structure in a later slice. A **"full"** department
has the complete set above.

---

## Standard agent specification

Every AI agent is defined in a single file under `agents/<division>/<agent-name>.md` and contains
these 11 sections, in order:

1. **Mission** — the one-sentence reason the agent exists
2. **Responsibilities** — what it owns
3. **Inputs** — what it consumes
4. **Outputs** — what it produces (structured)
5. **Tools** — what it is allowed to use
6. **Workflows** — how it operates, step by step
7. **Collaboration rules** — who it works with and how
8. **Escalation rules** — when it must hand off or ask for approval
9. **Quality standards** — the bar its output must meet
10. **KPIs** — how its performance is measured
11. **Review requirements** — who reviews its output before it is accepted

The empty scaffold lives at [agents/agent-template.md](agents/agent-template.md).

---

## Standard long-form document sections

Substantial standalone documents follow this section order (omit sections that do not apply, never
invent filler for them):

Purpose · Scope · Principles · Responsibilities · Inputs · Outputs · Workflows ·
Decision Frameworks · KPIs · Quality Standards · Automation · Templates · Checklists ·
Examples · References · Future Improvements

---

## Naming conventions

- **Files & folders:** lowercase, hyphen-separated — `incident-response.md`, `technical-debt/`.
- **Folders represent domains, not technologies** — `payments/`, not `controllers/`.
- **One concept per file.** If a file grows two distinct concerns, split it.
- **Every folder has a `README.md`** that indexes and orients.

---

## Authoring rules

- **No placeholder text.** Every document is written to be used by a real company.
- **Prefer depth over breadth.** A complete department beats twenty thin stubs.
- **Consistency of terminology** across the whole repository — see [GLOSSARY.md](GLOSSARY.md).
- **Cross-link liberally** using relative paths so the system stays navigable.
- **Integrate, don't isolate** — every component references how it connects to the rest.
