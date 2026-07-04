# Robotics - Added Workflow

Layered on top of the core [SDLC](../../workflows/sdlc.md), this domain adds:

```
Requirements (incl. safety envelope) -> hardware + firmware design
  -> perception/control models (sim -> HIL)
  -> integrated safety testing -> pilot fleet
  -> field deployment + OTA -> fleet monitoring/incidents
```

## How it maps to core

- Hardware and firmware use [hardware](../../hardware/README.md).
- Perception/control use [ai](../../ai/README.md) with sim + HIL evaluation.
- Field operations use [post-launch](../../post-launch/README.md) (fleet health, OTA, [incident response](../../post-launch/incident-response.md)).
- Safety and security use [security](../../security/README.md) and the hardware safety gate.
