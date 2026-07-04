# Roadmap

Company OS is now feature-complete as a framework: all 20 departments, 93 agents, 11 starter kits, the
guides, and CI are built. This page tracks what exists and the (now optional) directions for growth.

## ✅ Built

- **Foundation & conventions** — [hub README](../README.md), [STRUCTURE](../STRUCTURE.md), [CONTRIBUTING](../CONTRIBUTING.md), [GLOSSARY](../GLOSSARY.md), [department template](../templates/department-template/), [agent template](../agents/agent-template.md), [document templates](../templates/documents/).
- **Kernel** — [orchestration/](../orchestration/), [memory/](../memory/), [agents registry](../agents/README.md).
- **Identity & governance** — [company/](../company/), [governance/](../governance/).
- **All 20 departments, full structure** — engineering, product, post-launch, design, research, ai, strategy, security, devops, finance, legal, hr, operations, marketing, sales, customer-success, data, documentation, hardware, investor-relations. Each has the standard 18 files + `templates/`, `checklists/`, `examples/`.
- **93 agent specifications** across every division, each following the 11-section [standard spec](../agents/agent-template.md).
- **11 starter kits** — [ai-startup](../starter-kits/ai-startup/) plus [saas](../starter-kits/saas/), [developer-tools](../starter-kits/developer-tools/), [enterprise-b2b](../starter-kits/enterprise-b2b/), [marketplace](../starter-kits/marketplace/), [consumer-app](../starter-kits/consumer-app/), [robotics](../starter-kits/robotics/), [drone](../starter-kits/drone/), [embedded](../starter-kits/embedded/), [iot](../starter-kits/iot/), [research-lab](../starter-kits/research-lab/).
- **Shared systems** — [workflows/sdlc.md](../workflows/sdlc.md), [standards/](../standards/), [playbooks/](../playbooks/).
- **Guides** — [company-building-guide](company-building-guide.md), [onboarding-paths](onboarding-paths.md), [okrs](okrs.md), [example-company](example-company.md).
- **Community health & CI** — [.github/](../.github/) and docs-check workflows ([link integrity](../scripts/check-links.py) + [structure conformance](../scripts/check-structure.py)).

## 🧭 Optional next directions

The framework is complete; these deepen it rather than fill gaps.

| Direction | Value |
|---|---|
| More cross-department playbooks | Handling a customer complaint, scaling a team, international expansion. |
| More document templates | Employment agreement, MSA/DPA, sales proposal, QBR deck. |
| More starter kits | Fintech, healthtech, climate-tech, gaming, edtech — copy the [ai-startup](../starter-kits/ai-startup/) pattern. |
| Deeper worked examples | Add per-department worked examples beyond the current one each. |
| More CI | Markdown lint, spell-check, TOC generation, stale-issue bot. |
| Tooling | A CLI to scaffold a new department/agent from the templates. |

## Contributing

Pick any direction, copy the relevant template, and follow [CONTRIBUTING.md](../CONTRIBUTING.md). Run
`python scripts/check-links.py` and `python scripts/check-structure.py` before opening a PR. Propose new
areas via the [feature request template](../.github/ISSUE_TEMPLATE/feature_request.md).
