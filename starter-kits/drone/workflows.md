# Drone / UAV - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Requirements + regulatory scope -> airframe/avionics + firmware
  -> autonomy (sim -> tethered -> controlled flight)
  -> fail-safe + geofence testing -> certification
  -> operations + fleet monitoring + incident response
```

## How it maps to core

- Airframe/avionics use [hardware](../../hardware/README.md).
- Autonomy uses [ai](../../ai/README.md) with staged flight testing.
- Regulatory/airspace uses [legal compliance](../../legal/README.md).
- Operations and incidents use [post-launch](../../post-launch/README.md).
