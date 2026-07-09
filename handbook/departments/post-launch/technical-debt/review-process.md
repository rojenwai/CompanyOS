# Technical Debt — Review Process

## Cadence

A regular debt review (e.g. per sprint) run by the [Maintenance Manager](../../../../ai/agents/post-launch/maintenance-manager.md):

1. Ingest new items from the [Technical Debt Agent](../../../../ai/agents/post-launch/technical-debt-agent.md) and manual reports.
2. Re-[prioritize](prioritization.md) the backlog.
3. Confirm this cycle's repayment selection fits the reserved capacity.
4. Route repayment to the [Refactoring Agent](../../../../ai/agents/engineering/refactoring-agent.md) or owning engineer.

## Repayment review

Repayment changes go through the standard [engineering review](../../engineering/review-process.md) and
must keep the test suite green ([refactoring policy](../../engineering/refactoring-policy.md)).

## Reporting

Debt trend and repayment rate are reported on the [maintenance dashboard](../dashboards.md) via
[metrics](metrics.md).
