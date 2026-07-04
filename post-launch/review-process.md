# Post-Launch Review Process

## Change review
Maintenance changes (patches, dependency bumps, fixes) go through the standard
[engineering review](../engineering/review-process.md), with expedited paths for
[hotfixes](hotfix-policy.md). Security changes require the [Security Reviewer](../orchestration/security-reviewer.md).

## Postmortem review
Every [incident](incident-response.md) gets a blameless postmortem reviewed by the
[Maintenance Manager](../agents/post-launch/maintenance-manager.md); action items are tracked to closure.

## Operational review
A regular reliability review of [SLA](sla.md) attainment, incident trends, debt, and cost — feeding
[product evolution](product-evolution.md) and the [roadmap](../product/roadmap.md).
