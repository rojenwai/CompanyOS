# Post-Launch Dashboards

## Reliability dashboard
**Audience:** on-call + CTO · **Cadence:** real-time
Panels: uptime/SLA · error rate · latency p50/p95/p99 · saturation · open incidents.

## Maintenance dashboard
**Audience:** Maintenance Division · **Cadence:** daily
Panels: dependency freshness · open security findings · [debt trend](technical-debt/metrics.md) · backup status · doc drift.

## Customer health dashboard
**Audience:** support + product · **Cadence:** daily
Panels: ticket volume/resolution time · CSAT/NPS · churn · adoption.

## Cost dashboard
**Audience:** COO/CFO · **Cadence:** daily
Panels: infra cost · cost per customer/request · anomalies.

Sourced from [observability](observability.md) and [analytics](analytics.md); alerts via [automation](automation.md).
