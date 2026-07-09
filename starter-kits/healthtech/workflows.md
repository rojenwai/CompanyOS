# Health Tech - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Regulatory classification (device? which class?)
  -> clinical problem validation with clinicians
  -> privacy-by-design architecture (PHI)
  -> build under a quality system
  -> clinical validation / evidence generation [gate]
  -> regulatory submission or exemption
  -> launch -> post-market surveillance + adverse-event reporting
```

## How it maps to core

- Classification and privacy law use [legal](../../handbook/departments/legal/README.md).
- Clinical evidence uses [research](../../handbook/departments/research/README.md) and, for models, [TRL](../../handbook/departments/research/technology-readiness.md) + [AI evaluation](../../handbook/departments/ai-engineering/evaluation-and-testing.md).
- PHI controls use [security](../../handbook/departments/security/README.md).
- Post-market surveillance uses [post-launch monitoring](../../handbook/departments/post-launch/monitoring.md) and [incident response](../../handbook/departments/post-launch/incident-response.md).
