# Post-Launch Standards

- **Every release is reversible** — a tested [rollback](rollback.md) exists before deploy.
- **Detect before customers** — services meet [observability](observability.md) requirements (metrics, logs, traces).
- **Every incident has a postmortem** — root cause and action items recorded to [lessons-learned](../memory/lessons-learned.md).
- **Every fix has a test** — bugs ship with a reproducing test to prevent [regression](../agents/post-launch/regression-agent.md).
- **No silent removals** — features/APIs follow the [deprecation policy](deprecation-policy.md).
- **Debt is tracked** — per the [technical-debt policy](technical-debt/policy.md).
- **Backups are tested** — restores are verified, not assumed ([database maintenance](../agents/post-launch/database-maintenance-agent.md)).

Conformance is checked via [review-process.md](review-process.md), [monitoring](monitoring.md), and [automation](automation.md).
