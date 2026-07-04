# Post-Launch Quality Gates

## Deploy gate
Ship only when the [release checklist](../templates/documents/release-checklist.md) passes and a
tested [rollback](rollback.md) exists.

## Post-deploy gate
A release is only "healthy" once post-deploy checks (error rate, latency, saturation) are green in
[observability](observability.md); otherwise → [rollback](rollback.md).

## Incident-closed gate
An incident is closed only when service is verified restored **and** a postmortem with action items is filed.

## Deprecation gate
A capability is removed only after its [deprecation](deprecation-policy.md) window has elapsed and
usage has fallen below threshold.
