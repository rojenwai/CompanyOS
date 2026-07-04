# AI Engineering - Decision Frameworks

How decisions are made here. All decisions follow the company
[decision framework](../governance/decision-framework.md); these are the department-specific ones.

- **Prompt vs. fine-tune vs. train** - Prefer prompting + RAG; fine-tune only when evals justify it; train only with strong data and need.
- **Model size** - Smallest model that passes the eval bar at target latency and cost.
- **Autonomy vs. human-in-the-loop** - Autonomous only when objective is clear, safe, and confident; otherwise HITL ([approval engine](../orchestration/approval-engine.md)).

Reversible decisions are made fast and revisited; irreversible ones require review and are recorded in
[decision memory](../memory/decision-memory.md).
