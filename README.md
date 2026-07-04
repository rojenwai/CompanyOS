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

---

## How to use this repository

1. **Read the [company identity](company/)** — mission, vision, principles, structure, roles.
2. **Understand [governance](governance/)** — how decisions are made, reviewed, and approved.
3. **Learn the [orchestration kernel](orchestration/)** and **[memory system](memory/)** — how the AI agent workforce is coordinated.
4. **Adopt a department** — each department (e.g. [engineering](engineering/), [product](product/)) is ready to use as-is.
5. **Extend with a [starter kit](starter-kits/)** — a preconfigured company type that inherits core Company OS and adds domain-specific practice.
6. **Follow the conventions** in [STRUCTURE.md](STRUCTURE.md) to build the departments not yet fleshed out — every folder replicates the same pattern.

**Building or running a company for the first time?** Start with the
**[Company-Building Guide](docs/company-building-guide.md)** — the skills to learn and the full steps
to build and manage a company, each linked into the OS.

New here? See [STRUCTURE.md](STRUCTURE.md) for the map and [GLOSSARY.md](GLOSSARY.md) for the vocabulary.

---

## Repository map

### Core (the "kernel")
| Area | Purpose |
|---|---|
| [company/](company/) | Identity: mission, vision, principles, org structure, executive roles |
| [governance/](governance/) | Decision framework, communication rules, quality gates, definition of done |
| [orchestration/](orchestration/) | CEO agent, planner, coordinator, review & approval engines, execution lifecycle |
| [memory/](memory/) | Company / project / customer / knowledge memory, retrieval, retention, versioning |
| [agents/](agents/) | The AI agent registry + the standard agent specification |

### Departments (each a miniature operating manual)
All 20 departments are fully built: the standard 18 files + `templates/`, `checklists/`, `examples/`, and their AI agents.

| | | | |
|---|---|---|---|
| [engineering/](engineering/) | [product/](product/) | [post-launch/](post-launch/) | [design/](design/) |
| [research/](research/) | [ai/](ai/) | [strategy/](strategy/) | [security/](security/) |
| [devops/](devops/) | [finance/](finance/) | [legal/](legal/) | [hr/](hr/) |
| [operations/](operations/) | [marketing/](marketing/) | [sales/](sales/) | [customer-success/](customer-success/) |
| [data/](data/) | [documentation/](documentation/) | [hardware/](hardware/) | [investor-relations/](investor-relations/) |

### Shared systems
| Area | Purpose |
|---|---|
| [workflows/](workflows/) | Cross-department processes, incl. the [SDLC](workflows/sdlc.md) |
| [standards/](standards/) | Company-wide standards (naming, docs, reviews, APIs, security…) |
| [templates/](templates/) | Reusable [department](templates/department-template/) and [document](templates/documents/) templates |
| [playbooks/](playbooks/) | Operational playbooks (launch, incident, hiring, fundraising…) |
| [starter-kits/](starter-kits/) | 11 preconfigured company types ([ai-startup](starter-kits/ai-startup/), [saas](starter-kits/saas/), [enterprise-b2b](starter-kits/enterprise-b2b/), [marketplace](starter-kits/marketplace/), [robotics](starter-kits/robotics/), …) |
| [docs/](docs/) | Cross-cutting guides: the [Company-Building Guide](docs/company-building-guide.md), [onboarding paths](docs/onboarding-paths.md), [OKRs](docs/okrs.md), a [worked example](docs/example-company.md), and the [ROADMAP](docs/ROADMAP.md) |

---

## Design philosophy

- **Modular & industry-agnostic** — supports SaaS, AI, robotics, embedded, IoT, hardware, drones, healthcare, fintech, climate tech, research labs, developer tools, consumer, and enterprise.
- **Same structure everywhere** — every department uses the [standard structure](STRUCTURE.md#standard-department-structure); every agent uses the [standard spec](agents/agent-template.md). Predictability makes the system extensible.
- **Evidence over assumptions · first principles · long-term value** — see [company/principles.md](company/principles.md).
- **Production-ready, never placeholder** — every document is written to actually be used.

---

## Contributing & extending

Company OS is built incrementally. To add a department, copy [templates/department-template/](templates/department-template/)
and fill it in. To add an agent, copy [agents/agent-template.md](agents/agent-template.md). See
[CONTRIBUTING.md](CONTRIBUTING.md) for authoring conventions.

> The original single-file operating manual that seeded this repository was decomposed into the
> structure above. Its full text is preserved in git history (pre-decomposition `README.md`).

---

## License

Company OS is released under the [MIT License](LICENSE) — free to clone, customize, and use commercially.
