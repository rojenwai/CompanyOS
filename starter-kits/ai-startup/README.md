# Starter Kit: AI Startup

A company whose core product is an AI system (LLM app, agent product, ML service). This kit inherits
all of Company OS and adds what an AI-native product company specifically needs.

## What it inherits (unchanged)

- The full [company identity](../../handbook/company/), [governance](../../handbook/governance/), and [kernel](../../ai/orchestration/) ([memory](../../ai/memory/), [agents](../../ai/agents/)).
- The [engineering](../../handbook/departments/engineering/), [product](../../handbook/departments/product/), and [post-launch](../../handbook/departments/post-launch/) departments.
- The [SDLC](../../handbook/workflows/sdlc.md), [standards](../../handbook/standards/), [templates](../../handbook/templates/), and [strategy](../../handbook/departments/strategy/).

## What it adds / emphasizes

| Delta | File |
|---|---|
| AI-specific agents (LLM, ML, evaluation, data) | [agents.md](agents.md) |
| AI product & evaluation standards | [standards.md](standards.md) |
| The AI delivery lifecycle (data → eval → deploy → monitor drift) | [workflows.md](workflows.md) |
| How to stand this up | [getting-started.md](getting-started.md) |

## Why these deltas

An AI startup lives or dies on **evaluation, cost, and model reliability**. Core Company OS already
treats [AI as an engineering discipline](../../handbook/departments/ai-engineering/README.md); this kit makes evaluation gates,
prompt/model versioning, drift monitoring, and per-request cost first-class in the day-to-day workflow.

## Swapping this kit

To build a different company type (e.g. `saas` or `robotics`), copy this folder's structure and replace
the AI-specific deltas with your domain's — the inheritance model is identical.
