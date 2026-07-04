# DevOps - Automation

What is automated, and the guardrails on it.

- Fully automated build, test, and deploy pipelines
- Auto-rollback on failed post-deploy health checks
- Automated dependency and base-image updates with tests
- Infrastructure drift detection and cost alerts

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
