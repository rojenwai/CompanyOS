# Engineering Dashboards

How the [metrics](metrics.md) are surfaced.

## Delivery dashboard
**Audience:** engineering + CTO · **Cadence:** real-time / weekly rollup
Panels: deployment frequency · lead time · change-failure rate · MTTR (the DORA set).

## Quality dashboard
**Audience:** engineering · **Cadence:** per PR + weekly
Panels: coverage vs targets · open defects by severity · flaky-test count · [technical-debt](technical-debt-policy.md) trend.

## Reliability dashboard
**Audience:** engineering + [post-launch](../post-launch/README.md) · **Cadence:** real-time
Panels: uptime/SLA · error rate · latency (p50/p95/p99) · saturation. Sourced from
[observability](../post-launch/observability.md); alerts route via [automation](automation.md).
