# Technical Debt — Tracking

Debt that isn't tracked doesn't get repaid. Every debt item is recorded so it is visible and revisable.

## Debt item fields

- **Description** — what the debt is.
- **Location** — where in the system.
- **Type** — duplicate / dead code / outdated dep / architecture drift / smell / perf / doc drift.
- **Impact** — what it costs (risk, slowdown, bug-proneness).
- **Estimate** — effort to repay.
- **Origin** — when/why it was taken.
- **Status** — open / scheduled / in-progress / repaid.

## Sources

Recorded manually when a shortcut is taken, and detected automatically by the
[Technical Debt Agent](../../agents/post-launch/technical-debt-agent.md). Items are stored so trends
feed [metrics](metrics.md).
