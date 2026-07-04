# Security - Playbooks

Situational guides. Each names the trigger and the steps.

### Suspected breach

1. Activate the [security-breach playbook](../post-launch/playbooks/security-breach.md)
2. Contain (isolate, rotate credentials)
3. Assess scope and data impact
4. Notify per [legal](../legal/README.md) obligations
5. Eradicate, recover, and run a blameless postmortem

### Critical CVE in a dependency

1. Confirm exposure and exploitability
2. Apply the [dependency-vulnerability playbook](../post-launch/playbooks/dependency-vulnerability.md)
3. Patch or mitigate
4. Verify and deploy
5. Backport to supported versions
