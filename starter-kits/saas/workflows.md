# SaaS - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Signup -> self-serve onboarding (time-to-first-value)
  -> activation -> subscription billing
  -> usage-based health scoring -> retention/expansion
  -> churn prevention (loop back to value)
```

## How it maps to core

- Onboarding and health use [customer-success](../../handbook/departments/customer-success/README.md).
- Billing uses [finance revenue & billing](../../ai/agents/finance/revenue-billing-agent.md) reconciled monthly.
- Reliability uses [devops SRE](../../handbook/departments/devops/README.md) and [post-launch SLAs](../../handbook/departments/post-launch/sla.md).
- Activation/retention metrics use [product analytics](../../handbook/departments/product/analytics.md) and [data](../../handbook/departments/data/README.md).
