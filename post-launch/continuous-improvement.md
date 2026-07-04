# Continuous Improvement

Every release automatically triggers a learning loop that turns production reality into the next
iteration. This is the operational face of the [Continuous Improvement Engine](../orchestration/continuous-improvement-engine.md).

## The loop

```
Release
  ↓
Collect telemetry ([observability](observability.md))
  ↓
Analyze analytics ([analytics](analytics.md))
  ↓
Collect feedback ([customer-feedback](customer-feedback.md))
  ↓
Review bugs ([bug-management](bug-management.md))
  ↓
Prioritize improvements ([product prioritization](../product/decision-frameworks.md))
  ↓
Update roadmap ([roadmap](../product/roadmap.md))
  ↓
Plan sprint → Develop → Test → Deploy
```

## Output

Lessons recorded to [lessons-learned](../memory/lessons-learned.md); prioritized improvements added to
the [roadmap](../product/roadmap.md); updates to standards, prompts, and workflows.

**Failure without a recorded lesson is unacceptable.**
