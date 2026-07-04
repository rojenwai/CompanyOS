# Security - Automation

What is automated, and the guardrails on it.

- Secret scanning on every commit (block on hit)
- SCA/SAST/DAST in CI with severity gates
- Automated dependency-vulnerability PRs ([devops](../devops/README.md))
- Anomaly and intrusion alerting to on-call

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
