# Technical Debt — Repayment Plan

## Reserved capacity

Every sprint reserves a fixed fraction of capacity for debt repayment (e.g. 10–20%). This is a
standing commitment, not a "when we have time" afterthought.

## Selection

Each cycle, fill the reserved capacity with the highest-[priority](prioritization.md) items:

1. All **P0** items first (they can also block feature work entirely).
2. Then **P1** items until capacity is used.
3. **P2** items are batched opportunistically alongside related feature work.

## Execution

Repayment is executed by the [Refactoring Agent](../../agents/engineering/refactoring-agent.md) (with
tests) or the owning engineer, reviewed via [review-process](review-process.md), and the item is marked
repaid in [tracking](tracking.md).

## Guardrail

If debt is growing faster than it is repaid ([metrics](metrics.md)), escalate to increase reserved
capacity — persistent growth is a reliability risk.
