# IoT Platform - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Device + firmware -> secure provisioning/identity
  -> connectivity -> telemetry ingestion pipelines
  -> cloud analytics + alerts -> fleet OTA
  -> fleet monitoring + lifecycle management
```

## How it maps to core

- Devices/firmware use [hardware](../../handbook/departments/hardware/README.md).
- Telemetry and analytics use [data](../../handbook/departments/data/README.md).
- Device identity and security use [security](../../handbook/departments/security/README.md).
- Fleet infra and OTA use [devops](../../handbook/departments/devops/README.md) and [post-launch](../../handbook/departments/post-launch/README.md).
