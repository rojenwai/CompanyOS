# SLA — Service Levels

## Definitions

- **SLI (indicator)** — a measured signal (e.g. success rate, latency).
- **SLO (objective)** — the internal target for an SLI (e.g. 99.9% monthly availability, p95 < 300ms).
- **SLA (agreement)** — the customer-facing commitment, with remedies if breached.

## Example objectives

| Service tier | Availability SLO | Latency SLO |
|---|---|---|
| Critical | 99.95% | p95 < 300ms |
| Standard | 99.9% | p95 < 500ms |

## Error budgets

Each SLO implies an error budget. When the budget is being spent too fast, feature work pauses in
favor of reliability (coordinated with [engineering](../engineering/README.md)).

## Enforcement

SLIs are tracked via [observability](observability.md) and [monitoring](monitoring.md); breaches
trigger [incident response](incident-response.md) and, where customer-facing, the remedies in the SLA.
