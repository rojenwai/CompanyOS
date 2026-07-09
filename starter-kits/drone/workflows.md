# Drone / UAV - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Requirements + regulatory scope -> airframe/avionics + firmware
  -> autonomy (sim -> tethered -> controlled flight)
  -> fail-safe + geofence testing -> certification
  -> operations + fleet monitoring + incident response
```

## How it maps to core

- Airframe/avionics use [hardware](../../handbook/departments/hardware/README.md).
- Autonomy uses [ai](../../handbook/departments/ai-engineering/README.md) with staged flight testing.
- Regulatory/airspace uses [legal compliance](../../handbook/departments/legal/README.md).
- Operations and incidents use [post-launch](../../handbook/departments/post-launch/README.md).
