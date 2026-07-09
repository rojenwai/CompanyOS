# Fintech - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Regulatory scoping (license or partner bank)
  -> ledger + money-movement design (double-entry, idempotent)
  -> integrate rails (payments, banking, cards)
  -> KYC/AML + fraud controls
  -> security & compliance audit [gate]
  -> launch under permission
  -> daily reconciliation + fraud monitoring
```

## How it maps to core

- Licensing and regulation use [legal](../../handbook/departments/legal/README.md).
- Ledger, reconciliation, and treasury use [finance](../../handbook/departments/finance/README.md).
- PCI/security controls use [security](../../handbook/departments/security/README.md) and the [security review template](../../handbook/templates/documents/security-review.md).
- Fraud models use [data](../../handbook/departments/data/README.md); incidents use [post-launch](../../handbook/departments/post-launch/incident-response.md).
