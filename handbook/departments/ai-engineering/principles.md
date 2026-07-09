# AI Engineering - Principles

Non-negotiable. Every piece of work is judged against these.

1. **Never rely solely on an LLM's internal knowledge when external data is available.** Retrieve and ground.
2. **Evaluate before you ship.** No eval, no release ([evaluation-and-testing.md](evaluation-and-testing.md)).
3. **Version everything.** Prompts and models are versioned and rollback-able ([prompt memory](../../../ai/memory/prompt-memory.md)).
4. **Right-size the model.** Do not use the largest model if a smaller one suffices.
5. **Observe everything, log no secrets.** Token, latency, cost, and decision paths - never PII or keys.
6. **Human-in-the-loop for high-risk actions.** Financial, legal, irreversible, or customer-impacting.
7. **Never invent.** APIs, statistics, or facts - state uncertainty and retrieve instead.
