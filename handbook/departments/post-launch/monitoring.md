# Monitoring

The company continuously monitors every product so problems are detected before customers feel them.

## What we watch

Server health · CPU · memory · database · API latency · errors · crash reports · user analytics ·
business metrics · AI performance · security events · infrastructure cost · customer usage ·
feature adoption · churn.

## Alerting

| Level | Meaning | Response |
|---|---|---|
| **Critical** | Customer-impacting outage or data risk | Page on-call immediately; open [incident](incident-response.md) |
| **Major** | Degraded service, SLA at risk | On-call responds within the hour |
| **Minor** | Localized/non-urgent issue | Handled in normal maintenance |
| **Informational** | Awareness only | Logged, reviewed in trends |

## Ownership

Metrics come from [observability](observability.md); the [Performance Monitoring](../../../ai/agents/post-launch/performance-monitoring-agent.md)
and [Infrastructure Health](../../../ai/agents/post-launch/infrastructure-health-agent.md) agents watch continuously
and raise findings to the [Maintenance Manager](../../../ai/agents/post-launch/maintenance-manager.md). Alert
routing is defined in [automation.md](automation.md).
