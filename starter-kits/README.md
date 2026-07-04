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

| Starter kit | Status |
|---|---|
| [ai-startup/](ai-startup/) | ✅ Exemplar |
| saas · developer-tools · enterprise-b2b · marketplace · consumer-app · robotics · drone · embedded · hardware · iot · research-lab | 🧭 Planned — follow the ai-startup pattern |

## To add a starter kit

1. Create `starter-kits/<company-type>/`.
2. Write a `README.md` stating what it **inherits** and what it **adds/overrides**.
3. Add only the domain deltas (agents, standards, workflows, getting-started); link to core for everything else.
