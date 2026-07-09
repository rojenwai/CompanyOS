# Continuous Improvement Engine

Every completed unit of work feeds this engine so the organization gets better over time — the
principle [Continuous Improvement](../../handbook/company/principles.md) made mechanical.

## Loop

```
Outcome (shipped work, incident, experiment)
  │
  ▼
Collect telemetry + feedback
  │
  ▼
Analyze: what worked, what failed, what surprised us
  │
  ▼
Extract lessons → write to memory/lessons-learned.md
  │
  ▼
Update prompts, workflows, standards, evaluation datasets
  │
  ▼
Feed prioritized improvements into the roadmap (via CEO Agent)
```

## Inputs

Release telemetry; [incident reports](../../handbook/templates/documents/incident-report.md); experiment results;
customer feedback; review findings.

## Outputs

- Entries in [lessons-learned](../memory/lessons-learned.md).
- Proposed updates to [standards](../../handbook/standards/), [workflows](../../handbook/workflows/), and agent [prompts](../memory/prompt-memory.md).
- Roadmap improvement items for the [CEO Agent](ceo-agent.md).

## Rule

Failure without a recorded lesson is unacceptable. See the post-launch
[continuous improvement loop](../../handbook/departments/post-launch/README.md).
