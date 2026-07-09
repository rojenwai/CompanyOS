# AI Startup — Getting Started

A short path to stand up an AI startup on Company OS.

## 1. Adopt the core
Read the [company identity](../../handbook/company/README.md), [governance](../../handbook/governance/README.md), and the
[kernel](../../ai/orchestration/README.md) + [memory](../../ai/memory/README.md). These apply unchanged.

## 2. Validate the problem
Run [Stage 1–3 of the startup lifecycle](../../handbook/departments/strategy/startup-lifecycle.md) and
[product discovery](../../handbook/departments/product/discovery.md). **Start from a problem, not a model.**

## 3. Activate the AI Division
Create the [added agents](agents.md) from the [template](../../ai/agents/agent-template.md); wire them into
the [orchestration kernel](../../ai/orchestration/README.md).

## 4. Stand up evaluation early
Define your eval set and success metric **before** building ([workflows.md](workflows.md)); adopt the
[added standards](standards.md) so evaluation, versioning, and cost are gates from day one.

## 5. Build the MVP
Scope the smallest useful AI product ([MVP planning](../../ai/agents/product/mvp-planning-agent.md)); build
with [RAG](../../handbook/departments/ai-engineering/README.md#retrieval-augmented-generation-rag) grounding and versioned
[prompts](../../ai/memory/prompt-memory.md).

## 6. Ship and monitor
Use core [release management](../../handbook/departments/post-launch/release-management.md) and monitor quality, drift, and
cost ([dashboards](../../handbook/departments/post-launch/dashboards.md)). Iterate via the
[continuous improvement loop](../../handbook/departments/post-launch/continuous-improvement.md).

> Everything not listed here comes from core Company OS — this kit only adds the AI-specific deltas.
