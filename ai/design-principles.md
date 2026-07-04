# AI Design Principles

Every AI system must be:

- **Reliable** — behaves consistently and degrades gracefully.
- **Explainable** — its reasoning and sources can be inspected.
- **Observable** — instrumented for [monitoring](../post-launch/observability.md).
- **Modular** — specialist [agents](../agents/README.md), not a monolith.
- **Tool-driven** — prefers tools over guessing.
- **Memory-aware** — grounded in [memory](../memory/README.md) and retrieved knowledge.
- **Secure** — hardened against misuse ([ai-security.md](ai-security.md)).
- **Cost-efficient** — right-sized models and precise context.
- **Continuously evaluated** — measured against an [evaluation suite](evaluation-and-testing.md).

**Never rely solely on an LLM's internal knowledge when external data is available** — retrieve first
([RAG](README.md#retrieval-augmented-generation-rag)).
