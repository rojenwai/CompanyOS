# Roadmap

**The roadmap is complete.** Every direction previously listed has been built. Company OS is a finished,
self-verifying framework: 20 departments, 93 agents, 16 starter kits, 17 document templates, 11 playbooks,
the guides, the scaffolding CLI, and three CI checks.

This page now records what exists and how to extend it.

## ✅ Built

### Foundation
- [Hub README](README.md) · [CUSTOMIZE](CUSTOMIZE.md) · [STRUCTURE](STRUCTURE.md) · [CONTRIBUTING](CONTRIBUTING.md) · [GLOSSARY](GLOSSARY.md) · [CHANGELOG](CHANGELOG.md)
- **Two-sided layout** — [handbook/](handbook/README.md) (what humans read) and [ai/](ai/README.md) (what the AI workforce runs on), so customization is obvious.

### handbook/ — the reading side
- **Identity & governance** — [company/](handbook/company/) and [governance/](handbook/governance/).
- **All 20 departments, full structure** — engineering, product, post-launch, design, research, ai-engineering, strategy, security, devops, finance, legal, hr, operations, marketing, sales, customer-success, data, documentation, hardware, investor-relations. Each has the standard 18 files + `templates/`, `checklists/`, `examples/`, plus domain deep-dives (e.g. [TRL](handbook/departments/research/technology-readiness.md), [sales methodology](handbook/departments/sales/methodology.md), [pitching](handbook/departments/strategy/pitching.md)).
- **Shared systems** — [SDLC](handbook/workflows/sdlc.md), [standards/](handbook/standards/), [templates/](handbook/templates/).
- **11 cross-department playbooks** — brainstorming, validating an idea, building an MVP, launching, running a sprint, hiring an engineer, pitching to investors, fundraising, handling a customer complaint, scaling a team, international expansion. ([index](handbook/playbooks/README.md))
- **17 document templates** — PRD, RFC, ADR, incident report, research report, security review, release checklist, meeting notes, status report, OKR, one-pager, offer letter, employment agreement, board update, sales proposal, QBR, DPA. ([index](handbook/templates/documents/README.md))
- **Guides** — [company-building-guide](handbook/guides/company-building-guide.md), [onboarding-paths](handbook/guides/onboarding-paths.md), [okrs](handbook/guides/okrs.md), [example-company](handbook/guides/example-company.md).
- **Worked examples** — every department ships at least one; several ship two (ADR + RFC, PRD + user stories, discovery notes + objection handling, scorecard + interview debrief, runway model + budget variance).

### ai/ — the machine side
- **93 agent specifications** across 20 divisions, each following the 11-section [standard spec](ai/agents/agent-template.md), each division self-indexed.
- **Orchestration kernel** — [CEO agent](ai/orchestration/ceo-agent.md), planner, task decomposer, coordinator, four reviewers, approval/execution/improvement engines, execution lifecycle.
- **Memory system** — 14 memory types plus retrieval, retention, and versioning.

### 16 starter kits
[ai-startup](starter-kits/ai-startup/) · [saas](starter-kits/saas/) · [developer-tools](starter-kits/developer-tools/) · [enterprise-b2b](starter-kits/enterprise-b2b/) · [marketplace](starter-kits/marketplace/) · [consumer-app](starter-kits/consumer-app/) · [robotics](starter-kits/robotics/) · [drone](starter-kits/drone/) · [embedded](starter-kits/embedded/) · [iot](starter-kits/iot/) · [research-lab](starter-kits/research-lab/) · [fintech](starter-kits/fintech/) · [healthtech](starter-kits/healthtech/) · [climate-tech](starter-kits/climate-tech/) · [gaming](starter-kits/gaming/) · [edtech](starter-kits/edtech/)

### Tooling & CI
- **[scripts/scaffold.py](scripts/scaffold.py)** — scaffold a new department or agent from the templates.
- **Three CI checks**, run on every push and PR: [check-links.py](scripts/check-links.py) (link integrity), [check-structure.py](scripts/check-structure.py) (department + agent conformance), [check-conventions.py](scripts/check-conventions.py) (self-indexing folders, no placeholder text, markdown hygiene).
- **Community health** — [.github/](.github/): issue & PR templates, code of conduct, security policy, support, funding, and a stale-issue bot.

## Extending it

Company OS is designed to be forked and shaped, not to grow indefinitely here. To extend it for your
company, follow [CUSTOMIZE.md](CUSTOMIZE.md):

```bash
python scripts/scaffold.py department <name>          # a new department
python scripts/scaffold.py agent <department> <name>  # a new agent
```

Ideas that would still add value upstream: more starter kits (copy the [ai-startup](starter-kits/ai-startup/)
pattern), more worked examples, and translations. Propose them via the
[feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

## Contributing

Follow [CONTRIBUTING.md](CONTRIBUTING.md), and run all three checks before opening a PR:

```bash
python scripts/check-links.py && python scripts/check-structure.py && python scripts/check-conventions.py
```
