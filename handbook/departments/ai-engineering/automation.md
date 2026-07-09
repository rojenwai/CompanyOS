# AI Engineering - Automation

What is automated, and the guardrails on it.

- Automated evaluation suite in CI on every prompt/model change
- Automatic cost-per-request tracking and alerts
- Drift detection on production quality metrics
- Prompt regression tests on every prompt version

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../../../ai/orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
