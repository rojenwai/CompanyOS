# Playbook: Running a Sprint

**When to use:** the recurring build cadence for a delivery team.

1. **Plan** - pull the top-priority, [Ready](../engineering/definition-of-ready.md) items ([prioritization](../product/decision-frameworks.md)); commit only to what capacity allows; reserve capacity for [tech debt](../post-launch/technical-debt/repayment-plan.md).
2. **Kick off** - confirm each item has an owner, acceptance criteria, and no blocking dependencies ([initiative kickoff](../operations/checklists/initiative-kickoff-checklist.md)).
3. **Execute** - build against [engineering standards](../engineering/standards.md); daily async standup surfaces blockers with owners.
4. **Review work** - every change meets the [Definition of Done](../engineering/quality-gates.md) and passes [code review](../engineering/review-process.md) before merge.
5. **Ship** - release via [devops](../devops/README.md) / the [launch playbook](launching-a-product.md); each change is reversible.
6. **Demo** - show shipped work; gather feedback.
7. **Retro** - blameless; adopt exactly one improvement and record it in [lessons learned](../memory/lessons-learned.md).

**Success criteria:** committed, Ready work ships to the Definition of Done, with one improvement adopted.
**Escalate if:** the sprint is slipping → the [slipping-project playbook](../operations/playbooks.md).
