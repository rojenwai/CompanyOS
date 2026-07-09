# Documentation - Automation

What is automated, and the guardrails on it.

- Documentation drift detection against the codebase/specs
- Reference-doc generation from API specs
- Freshness monitoring and stale-doc alerts
- Search-gap detection (high-query, no-result)

**Guardrails:** never auto-apply irreversible or customer-impacting changes without
[approval](../../../ai/orchestration/approval-engine.md); every automated action is logged to
[observability](../post-launch/observability.md).
