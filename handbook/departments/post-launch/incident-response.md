# Incident Response

How the company handles production incidents. Blameless throughout — focus on systems and process.

## Severity

| Sev | Definition | Target response |
|---|---|---|
| SEV1 | Major outage / data loss / security breach | Immediate; all-hands |
| SEV2 | Significant degradation; SLA at risk | Minutes |
| SEV3 | Minor, localized impact | Hours |
| SEV4 | Negligible customer impact | Next business day |

## Process

1. **Detect** — [monitoring](monitoring.md) alert or report.
2. **Declare** — assign an Incident Commander; open an [incident report](../../templates/documents/incident-report.md).
3. **Mitigate** — restore service first (often [rollback](rollback.md) or [hotfix](hotfix-policy.md)).
4. **Communicate** — regular, honest status to stakeholders and customers.
5. **Resolve** — confirm full recovery via [observability](observability.md).
6. **Postmortem** — root cause, timeline, action items → [lessons-learned](../../../ai/memory/lessons-learned.md).

## Playbooks

Situation-specific guides live in [playbooks/](playbooks/) (outage, DB failure, security breach, …).

## Coordination

Incidents are coordinated through the [orchestration Coordinator](../../../ai/orchestration/coordinator.md);
irreversible remediation requires [approval](../../../ai/orchestration/approval-engine.md).
