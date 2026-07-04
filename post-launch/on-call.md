# On-Call

Who responds when something breaks, and how.

## Rotation

- A primary and a secondary on-call are always assigned.
- Rotations are humane: bounded shifts, handoffs documented, follow-the-sun where possible.
- AI [maintenance agents](agents.md) handle first-line detection and safe automated remediation; humans
  are paged for judgment, approvals, and anything irreversible.

## Duties

1. Acknowledge alerts within the target time for their [severity](monitoring.md).
2. Assess impact; open an [incident](incident-response.md) for Critical/Major.
3. Mitigate first (often [rollback](rollback.md)), diagnose second.
4. Communicate status to stakeholders/customers.
5. Hand off cleanly; ensure a postmortem is scheduled.

## Escalation

If the on-call cannot mitigate within the severity's target, escalate to the
[Maintenance Manager](../agents/post-launch/maintenance-manager.md) and, for major business/security
impact, to the [CEO Agent](../orchestration/ceo-agent.md) and human leadership.
