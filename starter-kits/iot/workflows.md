# IoT Platform - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Device + firmware -> secure provisioning/identity
  -> connectivity -> telemetry ingestion pipelines
  -> cloud analytics + alerts -> fleet OTA
  -> fleet monitoring + lifecycle management
```

## How it maps to core

- Devices/firmware use [hardware](../../hardware/README.md).
- Telemetry and analytics use [data](../../data/README.md).
- Device identity and security use [security](../../security/README.md).
- Fleet infra and OTA use [devops](../../devops/README.md) and [post-launch](../../post-launch/README.md).
