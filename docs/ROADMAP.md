# Roadmap

What Company OS contains today and what would make it the complete "company in a box." Built
incrementally, depth-first — every planned item replicates a pattern that already exists, so it is
replication, not invention.

## ✅ Built

- **Foundation & conventions** — [hub README](../README.md), [STRUCTURE](../STRUCTURE.md), [CONTRIBUTING](../CONTRIBUTING.md), [GLOSSARY](../GLOSSARY.md), [department template](../templates/department-template/), [agent template](../agents/agent-template.md), [document templates](../templates/documents/).
- **Kernel** — [orchestration/](../orchestration/), [memory/](../memory/), [agents registry](../agents/README.md).
- **Identity & governance** — [company/](../company/), [governance/](../governance/).
- **Full departments** — [engineering/](../engineering/), [product/](../product/), [post-launch/](../post-launch/) (with maintenance agents, [technical-debt/](../post-launch/technical-debt/), and [playbooks/](../post-launch/playbooks/)).
- **Seeded departments** — [design/](../design/), [research/](../research/), [ai/](../ai/), [strategy/](../strategy/).
- **Shared systems** — [workflows/sdlc.md](../workflows/sdlc.md), [standards/](../standards/), [playbooks/](../playbooks/).
- **Guide & starter kit** — [company-building-guide.md](company-building-guide.md), [starter-kits/ai-startup/](../starter-kits/ai-startup/).
- **Community health & CI** — [.github/](../.github/) (issue/PR templates, code of conduct, security, support, funding, docs-check workflow).

## 🧭 Planned — replicate the department template

Full-structure build-out of the remaining departments, each from [templates/department-template/](../templates/department-template/):

**marketing · sales · finance · legal · operations · hr · security · devops · customer-success · investor-relations · data**

…and upgrading the seeded departments (design, research, ai, strategy) to the full 18-file structure.

## 🧭 Planned — more starter kits

Following [starter-kits/ai-startup/](../starter-kits/ai-startup/): **saas · developer-tools ·
enterprise-b2b · marketplace · consumer-app · robotics · drone · embedded · hardware · iot · research-lab.**

## Recommended additions (to become the full "company pack")

| Add | Why it's worth it |
|---|---|
| **`hr/` + `operations/` departments** | Hiring, onboarding, culture, and PM are where founders lose the most time — high leverage. |
| **`finance/` department** (from strategy seed) | Runway/cash is the #1 company killer; deserves its own operating manual. |
| **`legal/` department** | Incorporation, IP, contracts, privacy — expensive to get wrong; templatize it. |
| **More document templates** | Offer letter, employment agreement, board update, OKR sheet, one-pager, sales proposal, MSA/DPA. |
| **More cross-department playbooks** | Hiring an engineer, running a sprint, handling a customer complaint, fundraising, scaling a team, international expansion. |
| **Onboarding path per role** | A "day 1 → day 30" checklist per department so new hires (or agents) ramp fast. |
| **OKR / goal-setting system** | A lightweight `metrics/` or `okrs/` area tying department metrics to company goals. |
| **Example company walkthrough** | One fictional company taken through every step end-to-end (a living [example](../engineering/examples/)). |
| **Automation via `.github/workflows/`** | Extend beyond docs-check: markdown lint, spell check, TOC generation, stale-issue bot. |
| **`CHANGELOG.md` + release process for the repo itself** | Version Company OS so adopters can track updates. |

## Contributing to the roadmap

Pick any 🧭 item, copy the relevant template, and follow [CONTRIBUTING.md](../CONTRIBUTING.md). Open an
issue with the [feature request template](../.github/ISSUE_TEMPLATE/feature_request.md) to propose new areas.
