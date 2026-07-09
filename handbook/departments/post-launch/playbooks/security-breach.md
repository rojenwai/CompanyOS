# Playbook: Security Breach

**When to use:** a suspected or confirmed security breach or active exploitation.

1. **Declare** a SEV1 [incident](../incident-response.md); involve the [Chief Security Officer](../../../company/roles.md).
2. **Contain:** isolate affected systems; revoke/rotate compromised credentials and keys.
3. **Preserve evidence** before remediation (logs, snapshots).
4. **Eradicate:** patch the vulnerability ([Security Patch Agent](../../../../ai/agents/post-launch/security-patch-agent.md)); close the entry point.
5. **Assess impact:** what data/systems were exposed?
6. **Notify:** legal/compliance obligations (breach disclosure) via [legal](../../../company/roles.md).
7. **Recover & monitor** for re-entry.
8. **Postmortem** → [lessons-learned](../../../../ai/memory/lessons-learned.md).

**Success criteria:** breach contained, entry closed, obligations met, evidence preserved.
**Escalate immediately:** breaches always require human leadership and legal ([approval](../../../../ai/orchestration/approval-engine.md)); a Security Reviewer block cannot be auto-overridden.
