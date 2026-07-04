# Design - Automation

What is automated, and the guardrails on it.

- Automated accessibility scanning in CI on UI changes
- Design-token sync from the design system toward code
- Visual regression checks on component changes
- Contrast checking in the design pipeline

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
