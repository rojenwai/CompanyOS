# AI Startup — Added Standards

These extend the core [engineering](../../engineering/standards.md) and [AI](../../ai/README.md)
standards with rules specific to shipping AI products.

## Evaluation is a release gate

No model or prompt change ships without passing the [evaluation suite](../../ai/evaluation-and-testing.md)
(accuracy, hallucination rate, safety, latency, cost). This joins the core
[quality gates](../../governance/quality-gates.md).

## Prompt & model versioning

- Every prompt is versioned in [prompt memory](../../memory/prompt-memory.md).
- Every deployed model has a recorded version and a **model card** (capabilities, limits, eval results).
- Rollback of a prompt/model is as easy as rollback of code ([rollback](../../post-launch/rollback.md)).

## Cost as a first-class metric

Track **cost per request** and **cost per resolved task** on the [dashboards](../../post-launch/dashboards.md).
Prefer the smallest sufficient model; cache and batch ([cost optimization](../../ai/README.md#cost-optimization)).
When building on Claude, default to the latest, most capable models and right-size per task.

## Grounding & safety

Retrieve before generating when accuracy matters ([RAG](../../ai/README.md#retrieval-augmented-generation-rag));
harden against prompt injection and jailbreaks ([AI security](../../ai/ai-security.md)); keep a human in
the loop for high-risk actions ([approval engine](../../orchestration/approval-engine.md)).
