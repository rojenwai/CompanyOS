# Technical Debt Policy

Technical debt is allowed **only if** it is: documented · estimated · prioritized · scheduled for repayment.

Every sprint allocates capacity for debt reduction.

## Rules

- No undocumented debt. If you take a shortcut, record it.
- Debt is tracked, prioritized, and repaid — the full tracking system lives in
  [post-launch/technical-debt/](../post-launch/technical-debt/), and the
  [Technical Debt Agent](../../../ai/agents/post-launch/technical-debt-agent.md) continuously detects new debt
  (duplicate code, dead code, outdated libraries, architecture drift, code smells, doc drift).
- Debt that threatens correctness, security, or reliability is repaid before new features.

This policy operationalizes the company principle [Long-Term Thinking](../../company/principles.md).
