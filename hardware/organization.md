# Hardware - Organization

## Reporting

The [CTO](../company/roles.md) owns hardware standards alongside software and AI.

```
CTO
|-- Firmware / Embedded - on-device software
|-- Electrical          - circuits, power, sensors
`-- Mechanical          - enclosure, structure, thermal
```

## Interfaces

| Works with | On |
|---|---|
| [Engineering](../engineering/README.md) | Firmware, device APIs, cloud connectivity |
| [AI](../ai/README.md) | On-device / edge inference |
| [Security](../security/README.md) | Device and firmware security |
| [Post-launch](../post-launch/README.md) | Field health, OTA updates, RMA |

## Where this plugs into the kernel

Work is decomposed and routed by the [coordinator](../orchestration/coordinator.md), reviewed at the
[quality gates](quality-gates.md), and its lasting knowledge persists to
[memory](../memory/README.md). Major decisions require cross-functional review before
[CEO Agent](../orchestration/ceo-agent.md) approval.
