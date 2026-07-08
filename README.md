# Company OS

> **The open-source operating system for AI-native technology companies.**
>
> Version: 2.0 · Clone it, customize it, and run a company from idea to global scale.

Company OS is not a prompt repository, a code template, or a business plan. It is the **central
source of truth** for how an AI-native company operates: organizational structure, engineering
culture, product development, research, operations, an AI-agent workforce, orchestration, memory,
standards, templates, playbooks, and domain-specific starter kits.

It is **industry-agnostic** and **modular**. Nothing assumes a specific business. Every department
is a self-contained miniature operating manual that follows the same structure, so the system is
predictable, extensible, and repeatable.

**Scale:** 20 full departments · 93 AI agents · 11 starter kits · every folder self-indexes via its own `README.md`.

---

## Folder structure

```
company-os/                        the repository root IS Company OS
│
├── company/                       identity: mission, vision, principles, structure, roles
├── governance/                    decision framework, quality gates, communication, definition of done
│
├── orchestration/                 the kernel: CEO agent, planner, engines, reviewers, lifecycle
├── memory/                        14 memory types + retrieval, retention, versioning
├── agents/                        AI agent registry (93 agents) + the standard agent spec
│   ├── engineering/  product/  post-launch/  design/  research/  ai/  strategy/
│   ├── security/  devops/  finance/  legal/  hr/  operations/  marketing/
│   └── sales/  customer-success/  data/  documentation/  hardware/  investor-relations/
│
├── engineering/ ┐                 ┌ 20 departments, each a full operating manual:
├── product/     │                 │   README · mission · vision · principles · organization
├── post-launch/ │                 │   roles · agents · workflows · playbooks · sops
├── design/      │  each contains  │   decision-frameworks · standards · review-process
├── research/    ├─ the standard ──┤   quality-gates · automation · metrics · dashboards · tools
├── ai/          │  18 files +     │   + templates/  checklists/  examples/
├── strategy/    │  3 subfolders   │
├── security/    │                 └ (+ domain deep-dives, e.g. research/technology-readiness.md,
├── devops/      │                     sales/methodology.md, strategy/pitching.md)
├── finance/     │
├── legal/       │   ... hr/  operations/  marketing/  sales/  customer-success/
└── ...          ┘       data/  documentation/  hardware/  investor-relations/
│
├── workflows/                     cross-department processes (the 20-phase SDLC)
├── standards/                     index of every company-wide standard
├── playbooks/                     step-by-step guides (brainstorm, MVP, launch, hiring, fundraising…)
├── templates/                     department-template/ + documents/ (PRD, RFC, ADR, OKR…)
├── starter-kits/                  11 company types (ai-startup, saas, robotics, iot, research-lab…)
│
├── docs/                          guides: company-building-guide, onboarding-paths, okrs, roadmap
├── scripts/                       CI tooling: check-links.py, check-structure.py
├── .github/                       issue/PR templates, community health, CI workflows
│
├── README.md   STRUCTURE.md   GLOSSARY.md   CONTRIBUTING.md   CHANGELOG.md   LICENSE
```

---

## Contents

- [Folder structure](#folder-structure)
- [Start here](#start-here)
- [Meta & conventions](#meta--conventions)
- [The kernel](#the-kernel) — company · governance · orchestration · memory · agents
- [Departments](#departments) — all 20
- [The founder journey](#the-founder-journey) — idea → validate → build → launch → sell → raise → scale
- [Shared systems](#shared-systems) — workflows · standards
- [Templates](#templates) · [Playbooks](#playbooks) · [Starter kits](#starter-kits) · [Guides & docs](#guides--docs)
- [Automation](#automation) · [Design philosophy](#design-philosophy) · [Contributing](#contributing--extending) · [License](#license)

---

## Start here

1. **First-time founder?** Read the **[Company-Building Guide](docs/company-building-guide.md)** — the skills to learn and the full steps to build and manage a company, each linked into the OS.
2. **Adopting the OS?** Read the [company identity](company/README.md) → [governance](governance/README.md) → the [kernel](orchestration/README.md) + [memory](memory/README.md).
3. **Building a specific kind of company?** Pick a [starter kit](#starter-kits).
4. **Navigating or extending?** See [STRUCTURE.md](STRUCTURE.md) (the map) and [GLOSSARY.md](GLOSSARY.md) (the vocabulary).

> Every directory has its own `README.md` that indexes its files. This page is the top-level index; follow any link to that area's index for the full detail.

---

## Meta & conventions

| File | Purpose |
|---|---|
| [STRUCTURE.md](STRUCTURE.md) | The repository map + naming & authoring conventions |
| [GLOSSARY.md](GLOSSARY.md) | Shared vocabulary |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add departments, agents, and docs |
| [CHANGELOG.md](CHANGELOG.md) | What changed, by version |
| [docs/ROADMAP.md](docs/ROADMAP.md) | What is built and where it goes next |
| [LICENSE](LICENSE) | MIT |

---

## The kernel

The reusable core every department and agent plugs into.

| Area | What's inside |
|---|---|
| [company/](company/README.md) | Identity — [mission](company/mission.md) · [vision](company/vision.md) · [principles](company/principles.md) · [structure](company/structure.md) · [roles](company/roles.md) |
| [governance/](governance/README.md) | [decision framework](governance/decision-framework.md) · [communication rules](governance/communication-rules.md) · [quality gates](governance/quality-gates.md) · [output format](governance/universal-output-format.md) · [failure handling](governance/failure-handling.md) · [definition of done](governance/definition-of-done.md) |
| [orchestration/](orchestration/README.md) | [CEO agent](orchestration/ceo-agent.md) · [planner](orchestration/planner.md) · [task decomposer](orchestration/task-decomposer.md) · [coordinator](orchestration/coordinator.md) · [memory](orchestration/memory-manager.md)/[knowledge](orchestration/knowledge-manager.md) managers · [reviewer](orchestration/reviewer.md) · [QA](orchestration/qa-reviewer.md)/[security](orchestration/security-reviewer.md)/[docs](orchestration/documentation-reviewer.md) reviewers · [approval](orchestration/approval-engine.md)/[execution](orchestration/execution-engine.md)/[improvement](orchestration/continuous-improvement-engine.md) engines · [lifecycle](orchestration/execution-lifecycle.md) |
| [memory/](memory/README.md) | 14 memory types (session → company, project, customer, research, decision, lessons-learned, prompt, knowledge-base…) + [context](memory/context-management.md) · [retrieval](memory/retrieval.md) · [retention & versioning](memory/retention-and-versioning.md) |
| [agents/](agents/README.md) | The full [agent registry](agents/README.md) (93 agents by division) + the [standard agent spec](agents/agent-template.md) |

---

## Departments

All 20 are fully built: the standard 18 files + `templates/`, `checklists/`, `examples/`, and their AI agents. Each folder's `README.md` is its own index.

| Department | What it owns |
|---|---|
| [engineering/](engineering/README.md) | Maintainable, tested, secure software; standards, review, delivery |
| [product/](product/README.md) | The *right* product — discovery, PRDs, prioritization, roadmap, PMF |
| [post-launch/](post-launch/README.md) | Reliability after ship — monitoring, incidents, maintenance, [tech debt](post-launch/technical-debt/), EOL |
| [design/](design/README.md) | Usable, accessible experiences; the [design system](design/design-system.md) |
| [research/](research/README.md) | What to build next — [ideation](research/ideation.md), [TRL](research/technology-readiness.md), [opportunity scoring](research/opportunity-scoring.md) |
| [ai/](ai/README.md) | AI as engineering — [RAG](ai/README.md), [evaluation](ai/evaluation-and-testing.md), [prompt versioning](ai/prompt-engineering.md), [AI security](ai/ai-security.md) |
| [strategy/](strategy/README.md) | Building the company — [lifecycle](strategy/startup-lifecycle.md), [market](strategy/market-analysis.md), [model](strategy/business-model.md), [unit economics](strategy/unit-economics.md), [GTM](strategy/go-to-market.md) |
| [security/](security/README.md) | Threat modeling, pen testing, vulnerability mgmt, compliance, privacy |
| [devops/](devops/README.md) | CI/CD, infrastructure-as-code, releases, reliability (DORA/SRE) |
| [finance/](finance/README.md) | Forecasting, budgeting, accounting, billing, runway, cost |
| [legal/](legal/README.md) | Contracts, IP, compliance, privacy & terms |
| [hr/](hr/README.md) | Recruiting, onboarding, performance, culture |
| [operations/](operations/README.md) | Cadences, project mgmt, process, vendor & knowledge mgmt |
| [marketing/](marketing/README.md) | Positioning, content/SEO, brand, growth, launches, [psychology](marketing/psychology.md) |
| [sales/](sales/README.md) | Selling — [method](sales/methodology.md), [psychology](sales/psychology.md), [channels](sales/channels.md), closing |
| [customer-success/](customer-success/README.md) | Onboarding, health scoring, retention, expansion |
| [data/](data/README.md) | Pipelines, the metrics layer, analytics, governance |
| [documentation/](documentation/README.md) | Product & API docs, knowledge base, freshness |
| [hardware/](hardware/README.md) | Firmware, electronics, mechanical, test — for physical products |
| [investor-relations/](investor-relations/README.md) | Investor updates, board governance, cap table |

---

## The founder journey

The end-to-end path a company travels, with the exact docs for each phase. The [Company-Building Guide](docs/company-building-guide.md) narrates the whole arc; this is the quick index.

| Phase | Go to |
|---|---|
| **0 · Brainstorm** | [research/ideation.md](research/ideation.md) · [playbook](playbooks/brainstorming-ideas.md) |
| **1 · Validate the idea** | [strategy/idea-validation.md](strategy/idea-validation.md) · [product discovery](product/discovery.md) · [playbook](playbooks/validating-an-idea.md) |
| **2 · Assess & rank** | [technology readiness (TRL)](research/technology-readiness.md) · [opportunity scoring](research/opportunity-scoring.md) · [market analysis](strategy/market-analysis.md) |
| **3 · Business model** | [business model & pricing](strategy/business-model.md) · [unit economics](strategy/unit-economics.md) |
| **4 · Build** | [SDLC](workflows/sdlc.md) · [MVP playbook](playbooks/building-an-mvp.md) · [engineering](engineering/README.md) · [design](design/README.md) |
| **5 · Launch** | [launch playbook](playbooks/launching-a-product.md) · [release management](post-launch/release-management.md) |
| **6 · Sell** | [how to sell](sales/methodology.md) · [buyer psychology](sales/psychology.md) · [where to sell](sales/channels.md) · [GTM](strategy/go-to-market.md) |
| **7 · Raise** | [pitching](strategy/pitching.md) · [finding investors](strategy/finding-investors.md) · [fundraising playbook](playbooks/fundraising.md) |
| **8 · Operate & scale** | [operating rhythm](docs/company-building-guide.md) · [OKRs](docs/okrs.md) · [continuous improvement](post-launch/continuous-improvement.md) |

---

## Shared systems

| Area | What's inside |
|---|---|
| [workflows/](workflows/README.md) | Cross-department processes, incl. the 20-phase [SDLC](workflows/sdlc.md) |
| [standards/](standards/README.md) | Index of every company-wide standard (coding, testing, security, API, DB, product, docs…) |

---

## Templates

Copy-and-fill scaffolds — see [templates/](templates/README.md).

- **[department-template/](templates/department-template/)** — the canonical 21-file department skeleton.
- **[agent-template.md](agents/agent-template.md)** — the 11-section agent spec.
- **[documents/](templates/documents/README.md):** [PRD](templates/documents/prd.md) · [RFC](templates/documents/rfc.md) · [ADR](templates/documents/adr.md) · [incident report](templates/documents/incident-report.md) · [research report](templates/documents/research-report.md) · [security review](templates/documents/security-review.md) · [release checklist](templates/documents/release-checklist.md) · [meeting notes](templates/documents/meeting-notes.md) · [status report](templates/documents/status-report.md) · [OKR](templates/documents/okr.md) · [one-pager](templates/documents/one-pager.md) · [offer letter](templates/documents/offer-letter.md) · [board update](templates/documents/board-update.md)

---

## Playbooks

Step-by-step guides for recurring situations — see [playbooks/](playbooks/README.md).

[brainstorming ideas](playbooks/brainstorming-ideas.md) · [validating an idea](playbooks/validating-an-idea.md) · [building an MVP](playbooks/building-an-mvp.md) · [launching a product](playbooks/launching-a-product.md) · [running a sprint](playbooks/running-a-sprint.md) · [hiring an engineer](playbooks/hiring-an-engineer.md) · [pitching to investors](playbooks/pitching-to-investors.md) · [fundraising](playbooks/fundraising.md)

Incident & reliability playbooks live in [post-launch/playbooks/](post-launch/playbooks/) (outage, security breach, rollback, and 9 more).

---

## Starter kits

Preconfigured company types that inherit core Company OS and add domain deltas — see [starter-kits/](starter-kits/README.md).

[ai-startup](starter-kits/ai-startup/) · [saas](starter-kits/saas/) · [developer-tools](starter-kits/developer-tools/) · [enterprise-b2b](starter-kits/enterprise-b2b/) · [marketplace](starter-kits/marketplace/) · [consumer-app](starter-kits/consumer-app/) · [robotics](starter-kits/robotics/) · [drone](starter-kits/drone/) · [embedded](starter-kits/embedded/) · [iot](starter-kits/iot/) · [research-lab](starter-kits/research-lab/)

---

## Guides & docs

Cross-cutting guides — see [docs/](docs/README.md).

| Doc | Purpose |
|---|---|
| [company-building-guide.md](docs/company-building-guide.md) | Skills to learn + steps to build and manage a company |
| [onboarding-paths.md](docs/onboarding-paths.md) | Day 1 → day 30 ramp for every role (human or agent) |
| [okrs.md](docs/okrs.md) | How goals & OKRs tie department metrics to the mission |
| [example-company.md](docs/example-company.md) | One fictional company taken through every step |
| [ROADMAP.md](docs/ROADMAP.md) | What's built and where it goes next |

---

## Automation

| Area | Purpose |
|---|---|
| [.github/](.github/) | Issue/PR templates, code of conduct, security, support, funding, and CI workflows |
| [scripts/](scripts/) | Repo tooling — [check-links.py](scripts/check-links.py) (link integrity) and [check-structure.py](scripts/check-structure.py) (structure conformance), run in CI |

---

## Design philosophy

- **Modular & industry-agnostic** — supports SaaS, AI, robotics, embedded, IoT, hardware, drones, healthcare, fintech, climate tech, research labs, developer tools, consumer, and enterprise.
- **Same structure everywhere** — every department uses the [standard structure](STRUCTURE.md#standard-department-structure); every agent uses the [standard spec](agents/agent-template.md). Predictability makes the system extensible.
- **Evidence over assumptions · first principles · long-term value** — see [company/principles.md](company/principles.md).
- **Production-ready, never placeholder** — every document is written to actually be used.

---

## Contributing & extending

Company OS is built incrementally. To add a department, copy [templates/department-template/](templates/department-template/)
and fill it in. To add an agent, copy [agents/agent-template.md](agents/agent-template.md). Run
`python scripts/check-links.py` and `python scripts/check-structure.py` before opening a PR. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the full conventions.

> The original single-file operating manual that seeded this repository was decomposed into the
> structure above. Its full text is preserved in git history (pre-decomposition `README.md`).

---

## License

Company OS is released under the [MIT License](LICENSE) — free to clone, customize, and use commercially.
