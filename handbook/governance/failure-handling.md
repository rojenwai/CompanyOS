# Failure Handling

If information is missing:

- identify the gap
- explain why it matters
- state assumptions clearly
- recommend how to validate

**Never fabricate unknown information.**

---

## Applied to agents

This is a governance rule that every [agent](../../ai/agents/agent-template.md) inherits through its
*escalation rules*: when required information is absent, the agent states its assumptions and
confidence, flags the gap, and (if the decision is significant) escalates rather than guessing.

This rule is the backbone of [hallucination prevention](../departments/ai-engineering/README.md) and of the company
principle [Evidence Over Assumptions](../company/principles.md).
