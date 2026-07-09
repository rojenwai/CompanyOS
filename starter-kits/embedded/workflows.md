# Embedded Systems - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Requirements (resource + reliability budgets) -> firmware + electronics
  -> HIL testing -> environmental validation
  -> pilot units -> production -> field OTA + monitoring
```

## How it maps to core

- Firmware/electronics use [hardware](../../handbook/departments/hardware/README.md).
- Device/cloud software uses [engineering](../../handbook/departments/engineering/README.md).
- OTA and field reliability use [post-launch](../../handbook/departments/post-launch/README.md).
- Device security uses [security](../../handbook/departments/security/README.md).
