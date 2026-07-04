# Embedded Systems - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Requirements (resource + reliability budgets) -> firmware + electronics
  -> HIL testing -> environmental validation
  -> pilot units -> production -> field OTA + monitoring
```

## How it maps to core

- Firmware/electronics use [hardware](../../hardware/README.md).
- Device/cloud software uses [engineering](../../engineering/README.md).
- OTA and field reliability use [post-launch](../../post-launch/README.md).
- Device security uses [security](../../security/README.md).
