# Product Automation

| Automation | Trigger | Action | Owner | HITL? |
|---|---|---|---|---|
| Feedback intake | New ticket/review/request | Classify and route to backlog | [Customer Journey Agent](../../../ai/agents/product/customer-journey-agent.md) | Review before commit |
| Metric alerts | Threshold breach | Notify PM (activation/retention/churn) | Product Ops | No |
| Experiment readout | Test completes | Summarize result vs decision rule | PM | Yes (decision) |
| Backlog hygiene | Schedule | Flag stale/unready items | Product Ops | No |

## Guardrails

Automation informs prioritization; it never auto-commits roadmap changes or customer-facing changes
without PM review and [approval](../../../ai/orchestration/approval-engine.md).
