# Example - Hardware Test Plan (excerpt)

> Worked example - illustrative, not a live record.

**Product:** Outdoor IoT sensor node.

| Test | Requirement | Method | Gate |
|---|---|---|---|
| Operating temp | -20C to 60C | Environmental chamber, 48h | Blocking |
| Ingress | IP67 | Immersion + dust | Blocking |
| Battery life | >= 2 years | Accelerated discharge model | Blocking |
| OTA recovery | No brick on power loss mid-update | Interrupted-update rig, 100 cycles | Blocking |

**Rule:** all blocking tests must pass before fabrication release; OTA recovery is safety-adjacent and cannot be waived.
