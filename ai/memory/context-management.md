# Context Management

How the [Memory Manager](../orchestration/memory-manager.md) assembles the right context for a task
without overloading it.

## What good context contains

- Current task and its acceptance criteria
- Relevant previous decisions ([decision memory](decision-memory.md))
- Applicable requirements, architecture, and constraints
- Relevant files and retrieved [knowledge](knowledge-base.md)

## What to leave out

Unrelated history, stale information, and low-relevance retrievals. **Do not overload context** —
precision beats volume; irrelevant context degrades reasoning and raises cost.

## Assembly rules

1. Start from the task's scope (which memory stores apply).
2. Retrieve by relevance, most-recent-and-authoritative first.
3. Bound the context to what the task needs; summarize long histories.
4. Record which context was used, to tune precision over time.

See [cost optimization](../../handbook/departments/ai-engineering/README.md) and [retrieval.md](retrieval.md).
