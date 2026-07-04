# Changelog

All notable changes to Company OS. The format is based on [Keep a Changelog](https://keepachangelog.com);
Company OS uses date-based versions since it is a living framework, not shipped software.

## [2.0] - 2026-07

### Added
- **Complete department coverage.** All 20 departments built to the full 18-file structure with
  subfolders: engineering, product, post-launch, design, research, ai, strategy, security, devops,
  finance, legal, hr, operations, marketing, sales, customer-success, data, documentation, hardware,
  investor-relations.
- **93 AI agent specifications**, each following the 11-section [standard spec](agents/agent-template.md).
- **11 starter kits** - ai-startup (exemplar) plus saas, developer-tools, enterprise-b2b, marketplace,
  consumer-app, robotics, drone, embedded, iot, research-lab.
- **The [Company-Building Guide](docs/company-building-guide.md)** - skills to learn and steps to build
  and manage a company; plus [onboarding paths](docs/onboarding-paths.md), [goals & OKRs](docs/okrs.md),
  and an [end-to-end worked example](docs/example-company.md).
- **Community health & CI** - `.github/` (issue/PR templates, code of conduct, security, support,
  funding) and docs-check workflows (link integrity + structure conformance).
- **More document templates** (OKR, offer letter, board update, one-pager) and **cross-department
  playbooks** (hiring an engineer, running a sprint, fundraising).
- Root [MIT LICENSE](LICENSE).

### Changed
- Repurposed the single-file operating manual into the modular Company OS: kernel (orchestration +
  memory + agents), governance, standards, workflows, templates, and playbooks.
- Upgraded the four seeded departments (design, research, ai, strategy) to full structure.

## [1.0]

### Added
- The original single-file "AI Company Operating Manual" (8 parts), preserved in git history.
