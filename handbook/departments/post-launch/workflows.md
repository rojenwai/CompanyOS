# Post-Launch Workflows

## Detect → respond
[Monitoring](monitoring.md) alert → [on-call](on-call.md) assess → declare [incident](incident-response.md)
if Sev1/2 → [mitigate](rollback.md) → resolve → postmortem → [lessons](../../../ai/memory/lessons-learned.md).

## Report → fix
Bug reported → [triage](bug-management.md) → prioritize → route to [engineering](../engineering/README.md)
or auto-fix → test → verify → close.

## Maintain (continuous)
[Maintenance agents](agents.md) scan continuously → findings to the
[Maintenance Manager](../../../ai/agents/post-launch/maintenance-manager.md) → safe automated changes or
engineering handoff → [review](review-process.md) → ship.

## Improve
Every release runs the [continuous improvement loop](continuous-improvement.md).

## Evolve → sunset
Periodic [product evolution](product-evolution.md) → continue / improve / [deprecate](deprecation-policy.md) / [retire](end-of-life.md).
