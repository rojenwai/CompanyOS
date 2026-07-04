# Post-Launch SOPs

## SOP-01: Acknowledge an alert
1. Ack within the [severity](monitoring.md) target. 2. Assess impact. 3. Open an [incident](incident-response.md) for Sev1/2.

## SOP-02: Run a postmortem
1. Use the [incident report](../templates/documents/incident-report.md) template. 2. Establish root cause (blameless). 3. Assign action items with owners/dates. 4. File to [lessons-learned](../memory/lessons-learned.md).

## SOP-03: Apply a dependency/security update
1. [Dependency](../agents/post-launch/dependency-update-agent.md)/[Security Patch](../agents/post-launch/security-patch-agent.md) agent opens a PR. 2. CI + [security review](../orchestration/security-reviewer.md). 3. Merge; deploy phased; verify.

## SOP-04: Deprecate a feature
Follow the [deprecation policy](deprecation-policy.md): decide → announce → migrate → support window → remove.
