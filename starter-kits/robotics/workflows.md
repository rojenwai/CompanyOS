# Robotics - Added Workflow

Layered on top of the core [SDLC](../../handbook/workflows/sdlc.md), this domain adds:

```
Requirements (incl. safety envelope) -> hardware + firmware design
  -> perception/control models (sim -> HIL)
  -> integrated safety testing -> pilot fleet
  -> field deployment + OTA -> fleet monitoring/incidents
```

## How it maps to core

- Hardware and firmware use [hardware](../../handbook/departments/hardware/README.md).
- Perception/control use [ai](../../handbook/departments/ai-engineering/README.md) with sim + HIL evaluation.
- Field operations use [post-launch](../../handbook/departments/post-launch/README.md) (fleet health, OTA, [incident response](../../handbook/departments/post-launch/incident-response.md)).
- Safety and security use [security](../../handbook/departments/security/README.md) and the hardware safety gate.
