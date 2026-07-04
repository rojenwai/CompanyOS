# Observability

The three pillars that make systems understandable in production: **metrics, logs, and traces.**

## Metrics
Numeric time series (latency p50/p95/p99, error rate, saturation, throughput) feeding
[monitoring](monitoring.md) and [dashboards](dashboards.md).

## Logs
Structured, leveled logs (TRACE→FATAL per [engineering standards](../engineering/standards.md)).
**Never log** passwords, secrets, API keys, credit cards, or personal data.

## Traces
Distributed traces to follow a request across services and find where latency or failure originates.

## Rules

- Every service emits metrics, logs, and traces by default.
- All automated actions by the [Execution Engine](../orchestration/execution-engine.md) and agents are logged.
- Observability data is retained per [retention policy](../memory/retention-and-versioning.md) and is the
  primary evidence for [incident](incident-response.md) root-cause analysis.
