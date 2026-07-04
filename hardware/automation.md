# Hardware - Automation

What is automated, and the guardrails on it.

- Automated hardware-in-the-loop and firmware test suites
- Fleet telemetry and health monitoring
- OTA update orchestration with canary and rollback
- BOM and component-lifecycle (EOL) alerts

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
