# Starter Kit: AI Startup

A company whose core product is an AI system (LLM app, agent product, ML service). This kit inherits
all of Company OS and adds what an AI-native product company specifically needs.

## What it inherits (unchanged)

- The full [company identity](../../company/), [governance](../../governance/), and [kernel](../../orchestration/) ([memory](../../memory/), [agents](../../agents/)).
- The [engineering](../../engineering/), [product](../../product/), and [post-launch](../../post-launch/) departments.
- The [SDLC](../../workflows/sdlc.md), [standards](../../standards/), [templates](../../templates/), and [strategy](../../strategy/).

## What it adds / emphasizes

| Delta | File |
|---|---|
| AI-specific agents (LLM, ML, evaluation, data) | [agents.md](agents.md) |
| AI product & evaluation standards | [standards.md](standards.md) |
| The AI delivery lifecycle (data → eval → deploy → monitor drift) | [workflows.md](workflows.md) |
| How to stand this up | [getting-started.md](getting-started.md) |

## Why these deltas

An AI startup lives or dies on **evaluation, cost, and model reliability**. Core Company OS already
treats [AI as an engineering discipline](../../ai/README.md); this kit makes evaluation gates,
prompt/model versioning, drift monitoring, and per-request cost first-class in the day-to-day workflow.

## Swapping this kit

To build a different company type (e.g. `saas` or `robotics`), copy this folder's structure and replace
the AI-specific deltas with your domain's — the inheritance model is identical.
