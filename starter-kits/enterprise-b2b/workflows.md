# Enterprise B2B - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Outbound/inbound -> discovery -> security review + POC
  -> procurement + MSA/DPA negotiation
  -> onboarding + SSO provisioning -> QBRs -> renewal/expansion
```

## How it maps to core

- Security review uses [security compliance](../../security/README.md) and the [security review template](../../templates/documents/security-review.md).
- Contracts use [legal](../../legal/README.md).
- Solution fit uses the [Sales Engineer Agent](../../agents/sales/sales-engineer-agent.md).
- Onboarding/renewals use [customer-success](../../customer-success/README.md).
