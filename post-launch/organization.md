# Organization

The Maintenance Division reports to the [COO](../company/roles.md) for operations and the
[CTO](../company/roles.md) for technical health, and is executed by the [maintenance agents](agents.md).

## Structure

```
Maintenance Manager
├── Bug Triage · Regression · Technical Debt (quality)
├── Dependency Update · Security Patch (supply chain & security)
├── Performance Monitoring · Infrastructure Health · Database Maintenance (reliability)
├── API Compatibility (contracts)
└── Documentation Maintenance (docs)
```

## Interfaces

| Interfaces with | For | Via |
|---|---|---|
| [engineering/](../engineering/) | fixes, refactors | bug/debt handoff, PRs |
| [product/](../product/) | feedback, requests, iteration | [feature-requests](feature-requests.md), [analytics](analytics.md) |
| [security](../orchestration/security-reviewer.md) | patches, breaches | [security-patch-agent](../agents/post-launch/security-patch-agent.md) |
| [orchestration/](../orchestration/) | incident coordination, approvals | Coordinator, Approval Engine |
