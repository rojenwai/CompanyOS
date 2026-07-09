# Goals & OKRs

How Company OS connects the [company mission](../company/mission.md) to what each department measures, so
everyone is pulling in the same direction. Lightweight by design: Objectives and Key Results, scored
quarterly, every KR backed by a real metric.

## The cascade

```
Company mission + vision  (company/)
   ↓  set annually
Company strategy + north-star  (strategy/, company scorecard)
   ↓  set quarterly
Department Objectives  (each dept's metrics.md)
   ↓
Key Results = specific department metrics with targets  (dashboards/)
   ↓
Sprint / initiative work  (operations/, engineering/, product/)
```

## Rules

- **Few objectives.** 2-4 per team per quarter. Focus beats coverage.
- **Every KR is a real metric.** It maps to a number on a [dashboard](../departments/post-launch/dashboards.md) with an
  owner - no un-instrumented aspirations. Use the [OKR template](../templates/documents/okr.md).
- **Honest scoring.** Score 0.0-1.0 at quarter end; ~0.7 is a healthy stretch. Sandbagging (always 1.0)
  and un-actioned misses both get corrected.
- **Aligned, not dictated.** Departments propose OKRs that ladder up to the company north-star; the
  [CEO Agent](../../ai/orchestration/ceo-agent.md) resolves conflicts.
- **Learn, don't hide.** Misses feed the [Continuous Improvement Engine](../../ai/orchestration/continuous-improvement-engine.md);
  decisions are recorded in [decision memory](../../ai/memory/decision-memory.md).

## Where each department's metrics live

Every department defines its measures in its own `metrics.md` and surfaces them in `dashboards.md` - e.g.
[engineering](../departments/engineering/metrics.md), [product](../departments/product/metrics.md), [sales](../departments/sales/metrics.md),
[customer-success](../departments/customer-success/metrics.md). OKR Key Results are drawn from these, so goals and
day-to-day measurement never diverge. The company scorecard rolls them up for the
[board](../templates/documents/board-update.md).
