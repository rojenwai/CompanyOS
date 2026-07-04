# Engineering Automation

What engineering automates, and where a human/agent stays in the loop.

| Automation | Trigger | Action | Owner | HITL? |
|---|---|---|---|---|
| CI pipeline | PR / push | Build · lint · test · security scan | Cloud Engineer | No (blocks merge on failure) |
| Coverage gate | PR | Fail if below [targets](testing-standards.md) | QA Engineer | No |
| Dependency scan | PR / schedule | Flag vulnerable/outdated deps | [Dependency Update Agent](../agents/post-launch/dependency-update-agent.md) | Review PRs |
| Deploy | Merge to release branch | Build → staging → prod (phased) | [Execution Engine](../orchestration/execution-engine.md) | **Yes** for production |
| Rollback | Failed health check | Revert to last good | Execution Engine | Auto + notify |

## Guardrails

Never automate an irreversible or customer-impacting action without recorded
[approval](../orchestration/approval-engine.md). All automated actions are logged
([observability](../post-launch/observability.md)); secrets are never logged.
