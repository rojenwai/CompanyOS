# AI Startup — Added Workflow: the AI delivery lifecycle

Layered on top of the core [SDLC](../../workflows/sdlc.md), AI features add a data-and-evaluation loop.

```
Problem + data availability
  ↓
Data pipeline (collect · clean · label)   ← Data Engineer
  ↓
Baseline + eval set (define the metric that means "good")   ← AI Evaluation Agent
  ↓
Build (prompt / RAG / model)   ← LLM / ML Engineer
  ↓
Evaluate against the suite (accuracy · hallucination · safety · latency · cost)
  ↓  (gate — must pass)
Ship (versioned prompt/model, model card)
  ↓
Monitor drift + cost in production   ← Performance Monitoring + AI Evaluation
  ↓
Degradation? → AI model degradation playbook → back to Build
```

## How it maps to core

- The **eval gate** is an AI-specific [quality gate](../../governance/quality-gates.md).
- **Ship** uses the core [release management](../../post-launch/release-management.md) and [rollback](../../post-launch/rollback.md).
- **Monitor drift** uses core [observability](../../post-launch/observability.md) plus the
  [AI model degradation playbook](../../post-launch/playbooks/ai-model-degradation.md).
- Learnings feed the core [continuous improvement loop](../../post-launch/continuous-improvement.md).
