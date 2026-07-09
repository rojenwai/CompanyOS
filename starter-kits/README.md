# Starter Kits

A starter kit is a **preconfigured company type** that inherits the core Company OS and adds
domain-specific practice. Clone the repo, pick a starter kit, and you have an operating system tuned to
your kind of company.

## Inheritance model

- **Inherit, don't duplicate.** A starter kit references core departments, agents, and standards; it
  only adds **deltas** — new agents, extra standards, adjusted workflows, and getting-started guidance.
- **Override explicitly.** When a starter kit changes a core rule, it says so and explains why.
- **Same conventions.** Kits follow [STRUCTURE.md](../STRUCTURE.md) and [CONTRIBUTING.md](../CONTRIBUTING.md).

## Available

| Starter kit | For |
|---|---|
| [ai-startup/](ai-startup/) | AI-native product companies (exemplar) |
| [saas/](saas/) | Multi-tenant subscription software |
| [developer-tools/](developer-tools/) | APIs, SDKs, CLIs, developer platforms |
| [enterprise-b2b/](enterprise-b2b/) | Selling to large organizations (compliance, procurement) |
| [marketplace/](marketplace/) | Two-sided supply/demand platforms |
| [consumer-app/](consumer-app/) | High-scale consumer apps (engagement, growth) |
| [robotics/](robotics/) | Autonomous physical robots (hardware + AI) |
| [drone/](drone/) | UAVs (safety-critical, regulated) |
| [embedded/](embedded/) | Firmware on constrained hardware |
| [iot/](iot/) | Fleets of connected devices + cloud |
| [research-lab/](research-lab/) | Research-first, IP-driven organizations |
| [fintech/](fintech/) | Moving, storing, or lending money (licensing, ledgers, fraud) |
| [healthtech/](healthtech/) | Patient care, clinical decisions, or health data |
| [climate-tech/](climate-tech/) | Energy, materials, carbon, decarbonisation (TRL-gated, MRV) |
| [gaming/](gaming/) | Games as a live product (fun, retention, live-ops) |
| [edtech/](edtech/) | Learning products (efficacy, accessibility, student data) |

Each kit inherits all of core Company OS and adds only its domain deltas (agents, standards, workflows,
getting-started). **Delete the kits you don't use** — see [CUSTOMIZE.md](../CUSTOMIZE.md).

## To add a starter kit

1. Create `starter-kits/<company-type>/`.
2. Write a `README.md` stating what it **inherits** and what it **adds/overrides**.
3. Add only the domain deltas (`agents.md`, `standards.md`, `workflows.md`, `getting-started.md`); link to core for everything else.
