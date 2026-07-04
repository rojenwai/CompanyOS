# Post-Launch Automation

| Automation | Trigger | Action | Owner agent | HITL? |
|---|---|---|---|---|
| Alert routing | Threshold breach | Page on-call by [severity](monitoring.md) | Monitoring | No |
| Auto-rollback | Failed post-deploy check | Revert to last good | [Execution Engine](../orchestration/execution-engine.md) | Auto + notify |
| Dependency PRs | New/vulnerable version | Open update PR | [Dependency Update Agent](../agents/post-launch/dependency-update-agent.md) | Review PR |
| Security patch | Advisory match | Open patch PR / escalate | [Security Patch Agent](../agents/post-launch/security-patch-agent.md) | Review + approve |
| Backup verify | Schedule | Run + test restore | [Database Maintenance Agent](../agents/post-launch/database-maintenance-agent.md) | Alert on fail |
| Debt scan | Schedule / PR | Detect debt, file items | [Technical Debt Agent](../agents/post-launch/technical-debt-agent.md) | No |
| Doc drift check | Change merged | Flag stale docs | [Documentation Maintenance Agent](../agents/post-launch/documentation-maintenance-agent.md) | No |

## Guardrails

Never auto-apply an irreversible or customer-impacting change without recorded
[approval](../orchestration/approval-engine.md). All automated actions are logged
([observability](observability.md)).
