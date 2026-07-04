# SaaS - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Signup -> self-serve onboarding (time-to-first-value)
  -> activation -> subscription billing
  -> usage-based health scoring -> retention/expansion
  -> churn prevention (loop back to value)
```

## How it maps to core

- Onboarding and health use [customer-success](../../customer-success/README.md).
- Billing uses [finance revenue & billing](../../agents/finance/revenue-billing-agent.md) reconciled monthly.
- Reliability uses [devops SRE](../../devops/README.md) and [post-launch SLAs](../../post-launch/sla.md).
- Activation/retention metrics use [product analytics](../../product/analytics.md) and [data](../../data/README.md).
