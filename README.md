# Company OS

> **The open-source operating system for AI-native technology companies.**
>
> Version: 2.1 · Clone it, customize it, and run a company from idea to global scale.

Company OS is not a prompt repository, a code template, or a business plan. It is the **central
source of truth** for how an AI-native company operates: organizational structure, engineering
culture, product development, research, operations, an AI-agent workforce, orchestration, memory,
standards, templates, playbooks, and domain-specific starter kits.

It is **industry-agnostic** and **modular**. Nothing assumes a specific business. Every department
is a self-contained miniature operating manual that follows the same structure, so the system is
predictable, extensible, and repeatable.

**Scale:** an [AI C-suite](ai/agents/executive/README.md) · 20 full departments · 107 AI agents · 16 starter kits · every folder self-indexes via its own `README.md`.

---

## Two sides, so it's easy to customize

The repository is split down the middle. Know which side you're on and customization is obvious:

| | [handbook/](handbook/README.md) — what humans **read** | [ai/](ai/README.md) — what the AI **runs on** |
|---|---|---|
| **Contains** | Company identity, governance, 20 department manuals, workflows, standards, playbooks, templates, guides | 107 agent specs (an executive C-suite + 20 divisions), the orchestration kernel, the memory system |
| **You edit it to** | Describe how *your* company works | Change which agents exist and how work is routed |
| **Audience** | Founders, employees, new hires | The agent workforce |

---

## How to customize

Company OS ships complete. Making it *yours* is mostly **deleting what you don't need** and **filling in
who you are**. Do it in this order:

**1. Make it your company** *(~30 min)* — edit these five files. They are the only place your identity is
defined; everything else refers back to them.
[mission](handbook/company/mission.md) · [vision](handbook/company/vision.md) · [principles](handbook/company/principles.md) · [structure](handbook/company/structure.md) · [roles](handbook/company/roles.md)

**2. Pick a starter kit** *(~10 min)* — choose the [kit](#starter-kits) matching your company type. It tells
you which departments to activate first and adds domain standards. Delete the other kits.

**3. Keep only the departments you need** *(~30 min)* — you don't need all twenty on day one. A typical
early-stage software company runs `product`, `engineering`, `design`, `post-launch`, `strategy`.
To remove one: delete `handbook/departments/<name>/` and `ai/agents/<name>/`, drop its rows from the
indexes, remove it from `DEPARTMENT_NAMES` in [scripts/check-structure.py](scripts/check-structure.py), then
run the checks below.
To add one: `python scripts/scaffold.py department <name>`.

**4. Choose your agents** *(~20 min)* — open [ai/agents/README.md](ai/agents/README.md), keep the agents
you'll actually run, delete the rest. To add one: `python scripts/scaffold.py agent <department> <agent-name>`.

**5. Tune the rules** *(ongoing)* — adjust [quality gates](handbook/governance/quality-gates.md), the
[decision framework](handbook/governance/decision-framework.md), and each department's `standards.md` to
match how strict you want to be.

### What to edit, at a glance

| | Files | Guidance |
|---|---|---|
| ✏️ **Always** | `handbook/company/*`, `ai/agents/*` | This *is* your company and your workforce |
| ⚙️ **Often** | department `standards.md`, `metrics.md`, `quality-gates.md`, `governance/*` | Tune to your bar |
| 📖 **Read, don't edit** | `handbook/guides/*` | Guidance for you, not config |
| 🔒 **Leave alone** | `handbook/templates/*`, `STRUCTURE.md`, `scripts/*`, `.github/*` | The framework that keeps it consistent |

### Verify your changes

```bash
python scripts/check-links.py        # every internal link resolves
python scripts/check-structure.py    # departments + agent specs conform
python scripts/check-conventions.py  # README per folder, no placeholder text
```

All three run in CI on every push and PR. If you removed a department, `check-links.py` points you at every
link that still references it.

👉 Full detail, including how to add a department or agent by hand: **[CUSTOMIZE.md](CUSTOMIZE.md)**.

---

## Folder structure

```
company-os/
│
├── handbook/                  ◀── EVERYTHING YOU READ ─────────────────────────
│   ├── company/                   identity: mission, vision, principles, structure, roles
│   ├── governance/                decision framework, quality gates, definition of done
│   │
│   ├── departments/               20 department manuals, each the same 18-file shape:
│   │   ├── engineering/  product/  design/  post-launch/  ai-engineering/
│   │   ├── research/  strategy/  data/  hardware/
│   │   ├── marketing/  sales/  customer-success/
│   │   └── operations/  hr/  finance/  legal/  security/  devops/
│   │       documentation/  investor-relations/
│   │           └─ README · mission · vision · principles · organization · roles
│   │              agents · workflows · playbooks · sops · decision-frameworks
│   │              standards · review-process · quality-gates · automation
│   │              metrics · dashboards · tools + templates/ checklists/ examples/
│   │
│   ├── workflows/                 cross-department processes (the 20-phase SDLC)
│   ├── standards/                 index of every company-wide standard
│   ├── playbooks/                 brainstorm · MVP · launch · sprint · hiring · fundraising
│   ├── templates/                 department-template/ + documents/ (PRD, RFC, ADR, OKR…)
│   └── guides/                    company-building-guide · onboarding-paths · okrs · example-company
│
├── ai/                        ◀── EVERYTHING THE AI RUNS ON ──────────────────
│   ├── agents/                    107 agent specs
│   │   ├── executive/             the C-suite: AI Co-Founder · CTO · CPO · COO · CFO · CMO · CRO
│   │   │                          Chief Designer/Scientist/Data/Security/Legal/People · Chief of Staff
│   │   └── engineering/ product/ post-launch/ design/ research/ ai-engineering/ …
│   │                              one folder per department, each reporting to its executive
│   ├── orchestration/             the kernel: CEO agent, planner, engines, reviewers
│   └── memory/                    14 memory types + retrieval, retention, versioning
│
├── starter-kits/              ◀── PICK YOUR COMPANY TYPE ────────────────────
│   └── ai-startup/ saas/ developer-tools/ enterprise-b2b/ marketplace/
│       consumer-app/ robotics/ drone/ embedded/ iot/ research-lab/
│
├── scripts/                       CI tooling: check-links.py, check-structure.py
├── .github/                       issue/PR templates, community health, CI workflows
│
└── README.md  CUSTOMIZE.md  STRUCTURE.md  GLOSSARY.md
    CONTRIBUTING.md  CHANGELOG.md  ROADMAP.md  LICENSE
```

---

## Contents

- [How to customize](#how-to-customize) · [Folder structure](#folder-structure)
- [Start here](#start-here) · [Meta & conventions](#meta--conventions)
- [handbook/ — the reading side](#handbook--the-reading-side)
- [ai/ — the machine side](#ai--the-machine-side)
- [The founder journey](#the-founder-journey) — idea → validate → build → launch → sell → raise → scale
- [Starter kits](#starter-kits) · [Automation](#automation)
- [Design philosophy](#design-philosophy) · [Contributing](#contributing--extending) · [License](#license)

---

## Start here

1. **First-time founder?** Read the **[Company-Building Guide](handbook/guides/company-building-guide.md)** — the skills to learn and the full steps to build and manage a company.
2. **Making this your company?** Follow **[CUSTOMIZE.md](CUSTOMIZE.md)**.
3. **Adopting the OS?** [company identity](handbook/company/README.md) → [governance](handbook/governance/README.md) → the [kernel](ai/orchestration/README.md) + [memory](ai/memory/README.md).
4. **Building a specific kind of company?** Pick a [starter kit](#starter-kits).

> Every directory has its own `README.md` that indexes it. This page is the top-level index; follow any link to that area's index for the full detail.

## Meta & conventions

| File | Purpose |
|---|---|
| [CUSTOMIZE.md](CUSTOMIZE.md) | How to make this repo your own |
| [STRUCTURE.md](STRUCTURE.md) | The repository map + naming & authoring conventions |
| [GLOSSARY.md](GLOSSARY.md) | Shared vocabulary |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add departments, agents, and docs |
| [CHANGELOG.md](CHANGELOG.md) · [ROADMAP.md](ROADMAP.md) | What changed · what's next |
| [LICENSE](LICENSE) | MIT |

---

## handbook/ — the reading side

Full index: **[handbook/README.md](handbook/README.md)**

| Area | What's inside |
|---|---|
| [company/](handbook/company/README.md) | [mission](handbook/company/mission.md) · [vision](handbook/company/vision.md) · [principles](handbook/company/principles.md) · [structure](handbook/company/structure.md) · [roles](handbook/company/roles.md) |
| [governance/](handbook/governance/README.md) | [decision framework](handbook/governance/decision-framework.md) · [quality gates](handbook/governance/quality-gates.md) · [communication rules](handbook/governance/communication-rules.md) · [definition of done](handbook/governance/definition-of-done.md) · [failure handling](handbook/governance/failure-handling.md) |
| [workflows/](handbook/workflows/README.md) | The 20-phase [SDLC](handbook/workflows/sdlc.md) |
| [standards/](handbook/standards/README.md) | Index of every company-wide standard |
| [templates/](handbook/templates/README.md) | [department template](handbook/templates/department-template/) · 17 [document templates](handbook/templates/documents/README.md): [PRD](handbook/templates/documents/prd.md) · [RFC](handbook/templates/documents/rfc.md) · [ADR](handbook/templates/documents/adr.md) · [incident report](handbook/templates/documents/incident-report.md) · [security review](handbook/templates/documents/security-review.md) · [release checklist](handbook/templates/documents/release-checklist.md) · [OKR](handbook/templates/documents/okr.md) · [one-pager](handbook/templates/documents/one-pager.md) · [offer letter](handbook/templates/documents/offer-letter.md) · [employment agreement](handbook/templates/documents/employment-agreement.md) · [board update](handbook/templates/documents/board-update.md) · [sales proposal](handbook/templates/documents/sales-proposal.md) · [QBR](handbook/templates/documents/qbr.md) · [DPA](handbook/templates/documents/dpa.md) |
| [playbooks/](handbook/playbooks/README.md) | [brainstorming](handbook/playbooks/brainstorming-ideas.md) · [validating an idea](handbook/playbooks/validating-an-idea.md) · [building an MVP](handbook/playbooks/building-an-mvp.md) · [launching](handbook/playbooks/launching-a-product.md) · [running a sprint](handbook/playbooks/running-a-sprint.md) · [hiring an engineer](handbook/playbooks/hiring-an-engineer.md) · [pitching](handbook/playbooks/pitching-to-investors.md) · [fundraising](handbook/playbooks/fundraising.md) · [customer complaint](handbook/playbooks/handling-a-customer-complaint.md) · [scaling a team](handbook/playbooks/scaling-a-team.md) · [international expansion](handbook/playbooks/international-expansion.md) |
| [guides/](handbook/guides/README.md) | [Company-Building Guide](handbook/guides/company-building-guide.md) · [onboarding paths](handbook/guides/onboarding-paths.md) · [OKRs](handbook/guides/okrs.md) · [worked example](handbook/guides/example-company.md) |

### Departments (20)

Full index: **[handbook/departments/README.md](handbook/departments/README.md)**

| Department | What it owns |
|---|---|
| [engineering/](handbook/departments/engineering/README.md) | Maintainable, tested, secure software; standards, review, delivery |
| [product/](handbook/departments/product/README.md) | The *right* product — discovery, PRDs, prioritization, roadmap, PMF |
| [post-launch/](handbook/departments/post-launch/README.md) | Reliability after ship — monitoring, incidents, maintenance, [tech debt](handbook/departments/post-launch/technical-debt/), EOL |
| [design/](handbook/departments/design/README.md) | Usable, accessible experiences; the [design system](handbook/departments/design/design-system.md) |
| [research/](handbook/departments/research/README.md) | What to build next — [ideation](handbook/departments/research/ideation.md), [TRL](handbook/departments/research/technology-readiness.md), [opportunity scoring](handbook/departments/research/opportunity-scoring.md) |
| [ai-engineering/](handbook/departments/ai-engineering/README.md) | Building AI products — RAG, [evaluation](handbook/departments/ai-engineering/evaluation-and-testing.md), [prompt standards](handbook/departments/ai-engineering/prompt-engineering.md), [AI security](handbook/departments/ai-engineering/ai-security.md) |
| [strategy/](handbook/departments/strategy/README.md) | Building the company — [lifecycle](handbook/departments/strategy/startup-lifecycle.md), [market](handbook/departments/strategy/market-analysis.md), [business model](handbook/departments/strategy/business-model.md), [unit economics](handbook/departments/strategy/unit-economics.md) |
| [security/](handbook/departments/security/README.md) | Threat modeling, pen testing, vulnerability mgmt, compliance, privacy |
| [devops/](handbook/departments/devops/README.md) | CI/CD, infrastructure-as-code, releases, reliability (DORA/SRE) |
| [finance/](handbook/departments/finance/README.md) | Forecasting, budgeting, accounting, billing, runway, cost |
| [legal/](handbook/departments/legal/README.md) | Contracts, IP, compliance, privacy & terms |
| [hr/](handbook/departments/hr/README.md) | Recruiting, onboarding, performance, culture |
| [operations/](handbook/departments/operations/README.md) | Cadences, project mgmt, process, vendor & knowledge mgmt |
| [marketing/](handbook/departments/marketing/README.md) | Positioning, content/SEO, brand, growth, [psychology](handbook/departments/marketing/psychology.md) |
| [sales/](handbook/departments/sales/README.md) | Selling — [method](handbook/departments/sales/methodology.md), [psychology](handbook/departments/sales/psychology.md), [channels](handbook/departments/sales/channels.md) |
| [customer-success/](handbook/departments/customer-success/README.md) | Onboarding, health scoring, retention, expansion |
| [data/](handbook/departments/data/README.md) | Pipelines, the metrics layer, analytics, governance |
| [documentation/](handbook/departments/documentation/README.md) | Product & API docs, knowledge base, freshness |
| [hardware/](handbook/departments/hardware/README.md) | Firmware, electronics, mechanical, test — for physical products |
| [investor-relations/](handbook/departments/investor-relations/README.md) | Investor updates, board governance, cap table |

---

## ai/ — the machine side

Full index: **[ai/README.md](ai/README.md)**

| Area | What's inside |
|---|---|
| [agents/](ai/agents/README.md) | The registry of **107 agent specs** + the [standard 11-section spec](ai/agents/agent-template.md) |
| [agents/executive/](ai/agents/executive/README.md) | The **AI C-suite** — [AI Co-Founder](ai/agents/executive/ai-cofounder-agent.md) · [CTO](ai/agents/executive/cto-agent.md) · [CPO](ai/agents/executive/cpo-agent.md) · [COO](ai/agents/executive/coo-agent.md) · [CFO](ai/agents/executive/cfo-agent.md) · [CRO](ai/agents/executive/cro-agent.md) · [CMO](ai/agents/executive/cmo-agent.md) · [Chief Designer](ai/agents/executive/chief-designer-agent.md) · [Chief Scientist](ai/agents/executive/chief-scientist-agent.md) · [CDO](ai/agents/executive/chief-data-officer-agent.md) · [CSO](ai/agents/executive/chief-security-officer-agent.md) · [CLO](ai/agents/executive/chief-legal-officer-agent.md) · [CPeO](ai/agents/executive/chief-people-officer-agent.md) · [Chief of Staff](ai/agents/executive/chief-of-staff-agent.md) |
| [orchestration/](ai/orchestration/README.md) | [CEO agent](ai/orchestration/ceo-agent.md) · [planner](ai/orchestration/planner.md) · [task decomposer](ai/orchestration/task-decomposer.md) · [coordinator](ai/orchestration/coordinator.md) · [reviewer](ai/orchestration/reviewer.md) · [QA](ai/orchestration/qa-reviewer.md)/[security](ai/orchestration/security-reviewer.md)/[docs](ai/orchestration/documentation-reviewer.md) reviewers · [approval](ai/orchestration/approval-engine.md)/[execution](ai/orchestration/execution-engine.md)/[improvement](ai/orchestration/continuous-improvement-engine.md) engines · [lifecycle](ai/orchestration/execution-lifecycle.md) |
| [memory/](ai/memory/README.md) | 14 memory types (session → company, project, customer, decision, [lessons-learned](ai/memory/lessons-learned.md), [prompt](ai/memory/prompt-memory.md), [knowledge base](ai/memory/knowledge-base.md)…) + [context](ai/memory/context-management.md) · [retrieval](ai/memory/retrieval.md) · [retention & versioning](ai/memory/retention-and-versioning.md) |

> Don't confuse `ai/` (the AI **workforce**) with [handbook/departments/ai-engineering/](handbook/departments/ai-engineering/README.md) (the **discipline** of building AI products).

---

## The founder journey

The end-to-end path a company travels, with the exact doc for each phase. The [Company-Building Guide](handbook/guides/company-building-guide.md) narrates the whole arc.

| Phase | Go to |
|---|---|
| **0 · Brainstorm** | [ideation](handbook/departments/research/ideation.md) · [playbook](handbook/playbooks/brainstorming-ideas.md) |
| **1 · Validate the idea** | [idea validation](handbook/departments/strategy/idea-validation.md) · [product discovery](handbook/departments/product/discovery.md) · [playbook](handbook/playbooks/validating-an-idea.md) |
| **2 · Assess & rank** | [technology readiness (TRL)](handbook/departments/research/technology-readiness.md) · [opportunity scoring](handbook/departments/research/opportunity-scoring.md) · [market analysis](handbook/departments/strategy/market-analysis.md) |
| **3 · Business model** | [business model & pricing](handbook/departments/strategy/business-model.md) · [unit economics](handbook/departments/strategy/unit-economics.md) |
| **4 · Build** | [SDLC](handbook/workflows/sdlc.md) · [MVP playbook](handbook/playbooks/building-an-mvp.md) · [engineering](handbook/departments/engineering/README.md) · [design](handbook/departments/design/README.md) |
| **5 · Launch** | [launch playbook](handbook/playbooks/launching-a-product.md) · [release management](handbook/departments/post-launch/release-management.md) |
| **6 · Sell** | [how to sell](handbook/departments/sales/methodology.md) · [buyer psychology](handbook/departments/sales/psychology.md) · [where to sell](handbook/departments/sales/channels.md) · [GTM](handbook/departments/strategy/go-to-market.md) |
| **7 · Raise** | [pitching](handbook/departments/strategy/pitching.md) · [finding investors](handbook/departments/strategy/finding-investors.md) · [fundraising playbook](handbook/playbooks/fundraising.md) |
| **8 · Operate & scale** | [operating rhythm](handbook/guides/company-building-guide.md) · [OKRs](handbook/guides/okrs.md) · [continuous improvement](handbook/departments/post-launch/continuous-improvement.md) |

---

## Starter kits

Preconfigured company types that inherit core Company OS and add domain deltas — see [starter-kits/](starter-kits/README.md).

[ai-startup](starter-kits/ai-startup/) · [saas](starter-kits/saas/) · [developer-tools](starter-kits/developer-tools/) · [enterprise-b2b](starter-kits/enterprise-b2b/) · [marketplace](starter-kits/marketplace/) · [consumer-app](starter-kits/consumer-app/) · [robotics](starter-kits/robotics/) · [drone](starter-kits/drone/) · [embedded](starter-kits/embedded/) · [iot](starter-kits/iot/) · [research-lab](starter-kits/research-lab/) · [fintech](starter-kits/fintech/) · [healthtech](starter-kits/healthtech/) · [climate-tech](starter-kits/climate-tech/) · [gaming](starter-kits/gaming/) · [edtech](starter-kits/edtech/)

## Automation

| Script | Purpose |
|---|---|
| [scripts/scaffold.py](scripts/scaffold.py) | Scaffold a new department or agent from the templates |
| [scripts/check-links.py](scripts/check-links.py) | Every internal link resolves |
| [scripts/check-structure.py](scripts/check-structure.py) | Departments and agent specs conform |
| [scripts/check-conventions.py](scripts/check-conventions.py) | Every folder self-indexes; no placeholder text |

The three checkers run in CI on every push and PR ([.github/](.github/), which also holds issue/PR
templates, code of conduct, security policy, support, funding, and a stale-issue bot).

---

## Design philosophy

- **Two clean sides** — [handbook/](handbook/README.md) for humans, [ai/](ai/README.md) for the agent workforce. Customization is obvious because the boundary is obvious.
- **Modular & industry-agnostic** — supports SaaS, AI, robotics, embedded, IoT, hardware, drones, healthcare, fintech, climate tech, research labs, developer tools, consumer, and enterprise.
- **Same structure everywhere** — every department uses the [standard structure](STRUCTURE.md#standard-department-structure); every agent uses the [standard spec](ai/agents/agent-template.md). Predictability makes the system extensible.
- **Evidence over assumptions · first principles · long-term value** — see [handbook/company/principles.md](handbook/company/principles.md).
- **Production-ready, never placeholder** — every document is written to actually be used.

---

## Contributing & extending

To add a department, copy [handbook/templates/department-template/](handbook/templates/department-template/)
and fill it in. To add an agent, copy [ai/agents/agent-template.md](ai/agents/agent-template.md). Run
`python scripts/check-links.py` and `python scripts/check-structure.py` before opening a PR. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the full conventions.

> The original single-file operating manual that seeded this repository was decomposed into the
> structure above. Its full text is preserved in git history (pre-decomposition `README.md`).

---

## License

Company OS is released under the [MIT License](LICENSE) — free to clone, customize, and use commercially.
