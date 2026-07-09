# Playbooks

Company-wide operational playbooks for recurring situations. Incident and reliability playbooks live
with the department that runs them, in [post-launch/playbooks/](../departments/post-launch/playbooks/).

## Cross-department playbooks

| Playbook | Situation |
|---|---|
| [brainstorming-ideas.md](brainstorming-ideas.md) | Generating a pool of company/product ideas (Stage 0) |
| [validating-an-idea.md](validating-an-idea.md) | Validating an idea cheaply before building |
| [building-an-mvp.md](building-an-mvp.md) | Scoping and shipping a first version |
| [launching-a-product.md](launching-a-product.md) | Taking a product from ready to launched |
| [running-a-sprint.md](running-a-sprint.md) | The recurring build cadence |
| [hiring-an-engineer.md](hiring-an-engineer.md) | Adding engineering capacity, rigorously |
| [pitching-to-investors.md](pitching-to-investors.md) | Pitching to raise capital |
| [fundraising.md](fundraising.md) | Raising capital (or deciding not to) |
| [handling-a-customer-complaint.md](handling-a-customer-complaint.md) | An unhappy customer |
| [scaling-a-team.md](scaling-a-team.md) | Growing headcount without losing what works |
| [international-expansion.md](international-expansion.md) | Entering a new country |

## Operational playbooks (in their departments)

| Situation | Playbook |
|---|---|
| Handling an incident / outage | [post-launch/playbooks/critical-outage.md](../departments/post-launch/playbooks/critical-outage.md) |
| Security breach | [post-launch/playbooks/security-breach.md](../departments/post-launch/playbooks/security-breach.md) |
| Emergency hotfix / rollback | [post-launch/playbooks/emergency-hotfix.md](../departments/post-launch/playbooks/emergency-hotfix.md) · [rollback.md](../departments/post-launch/playbooks/rollback.md) |
| Engineering-time situations (failing CI, flaky test, large refactor) | [engineering/playbooks.md](../departments/engineering/playbooks.md) |
| Product situations (no PMF, unadopted feature) | [product/playbooks.md](../departments/product/playbooks.md) |

## Adding a playbook

Every playbook names the **trigger** ("when to use"), numbered **steps** that link into the departments
that own the work, and the **success criteria** plus an **escalate if**. Department-specific situations
belong in that department's `playbooks.md` instead.
