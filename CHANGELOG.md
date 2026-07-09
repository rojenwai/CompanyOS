# Changelog

All notable changes to Company OS. The format is based on [Keep a Changelog](https://keepachangelog.com);
Company OS uses date-based versions since it is a living framework, not shipped software.

## [2.2] - 2026-07 — roadmap complete

### Added
- **5 more starter kits** (16 total): [fintech](starter-kits/fintech/), [healthtech](starter-kits/healthtech/),
  [climate-tech](starter-kits/climate-tech/), [gaming](starter-kits/gaming/), [edtech](starter-kits/edtech/).
- **3 more cross-department playbooks** (11 total): handling a customer complaint, scaling a team,
  international expansion.
- **4 more document templates** (17 total): employment agreement, DPA, sales proposal, QBR.
- **Deeper worked examples** — a second example for engineering (RFC), product (user stories), sales
  (objection handling), hr (interview debrief), and finance (budget variance).
- **[scripts/scaffold.py](scripts/scaffold.py)** — a CLI to scaffold a new department or agent from the templates.
- **[scripts/check-conventions.py](scripts/check-conventions.py)** — a third CI check: every folder
  self-indexes, no placeholder text, markdown hygiene. Now wired into `docs-check.yml`.
- **Stale-issue bot** (`.github/workflows/stale.yml`).
- A **"How to customize"** section in the root README, and `README.md` files for all 20 agent divisions
  and `post-launch/technical-debt/`.

### Changed
- [ROADMAP.md](ROADMAP.md) rewritten: every previously planned direction is now built.

## [2.1] - 2026-07

### Changed — repository split into two sides, for easy customization
- **`handbook/`** now holds everything humans read: `company/`, `governance/`, all 20 department
  manuals under `handbook/departments/`, `workflows/`, `standards/`, `playbooks/`, `templates/`, and
  `guides/` (formerly `docs/`).
- **`ai/`** now holds everything the AI workforce runs on: `agents/` (93 specs), `orchestration/`, and
  `memory/`.
- The AI *department* (the discipline of building AI products) was renamed to
  `handbook/departments/ai-engineering/` to free the top-level `ai/` name for the agent workforce.
  Its agent folder moved to `ai/agents/ai-engineering/`.
- `docs/ROADMAP.md` moved to `ROADMAP.md` at the repository root.
- All ~4,200 internal links were remapped; both CI checks pass.

### Added
- **[CUSTOMIZE.md](CUSTOMIZE.md)** — a step-by-step guide to making the repo your own: what to edit
  always, what to tune, what to read, and what to leave alone; plus how to add or remove a department
  or an agent.
- Index pages for each side: [handbook/README.md](handbook/README.md),
  [handbook/departments/README.md](handbook/departments/README.md), and [ai/README.md](ai/README.md).
- A folder-structure diagram in the root README.

### Fixed
- Updated GitHub URLs after the repository was renamed to `CompanyOS`.

## [2.0] - 2026-07

### Added
- **Complete department coverage.** All 20 departments built to the full 18-file structure with
  subfolders: engineering, product, post-launch, design, research, ai, strategy, security, devops,
  finance, legal, hr, operations, marketing, sales, customer-success, data, documentation, hardware,
  investor-relations.
- **93 AI agent specifications**, each following the 11-section [standard spec](ai/agents/agent-template.md).
- **11 starter kits** - ai-startup (exemplar) plus saas, developer-tools, enterprise-b2b, marketplace,
  consumer-app, robotics, drone, embedded, iot, research-lab.
- **The [Company-Building Guide](handbook/guides/company-building-guide.md)** - skills to learn and steps to build
  and manage a company; plus [onboarding paths](handbook/guides/onboarding-paths.md), [goals & OKRs](handbook/guides/okrs.md),
  and an [end-to-end worked example](handbook/guides/example-company.md).
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
