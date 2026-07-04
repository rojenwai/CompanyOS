# Prompt Memory

**Scope:** reusable, versioned agent prompts, long-lived.

## What's stored
The canonical prompts for each agent and task type, with versions and evaluation results.

## Lifetime
Permanent and versioned; improvements are tracked against evaluation datasets.

## Writers / readers
Updated by the [Continuous Improvement Engine](../orchestration/continuous-improvement-engine.md) following the [prompt engineering standards](../ai/README.md); read by agents at instantiation.

## Rule
Prompt changes are evaluated (prompt regression tests) before they become canonical — see [AI testing](../ai/README.md).
