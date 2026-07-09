# Agent Template

> Copy this file to `agents/<division>/<agent-name>.md` and complete **all 11 sections**. An agent
> spec is considered incomplete if any section is missing. See [STRUCTURE.md](../../STRUCTURE.md#standard-agent-specification).

# <Agent Name>

**Division:** <Research | Product | Business | Design | Engineering | AI | Hardware | Security | DevOps | Data | Documentation | Marketing | Sales | Finance | Legal | Investor Relations | Orchestration | Post-Launch>
**Reports to:** <supervising agent or executive>

---

## 1. Mission

One sentence: the reason this agent exists and the outcome it is accountable for.

## 2. Responsibilities

- What this agent owns end-to-end.
- The concrete deliverables it is on the hook for.
- What it explicitly does **not** do (hand-offs).

## 3. Inputs

- The information, artifacts, and signals it consumes.
- Where each input comes from (which agent, memory store, or tool).

## 4. Outputs

Structured deliverables this agent produces. Every output should state its format and destination.

- Output → format → consumer.

## 5. Tools

- The tools/services the agent may use (search, database, code execution, APIs, hardware…).
- Any tool it is **prohibited** from using.
- Rule: never fabricate tool outputs.

## 6. Workflows

Step-by-step operating procedure(s):

1. …
2. …
3. …

## 7. Collaboration rules

- Which agents it works with, and the interface for each.
- What it must review from others / submit to others.
- No agent operates independently on major decisions.

## 8. Escalation rules

- Conditions that require escalation to a supervisor or the CEO Agent.
- Conditions that require [Human-in-the-Loop](../../handbook/governance/README.md) approval.
- What to do when required information is missing (state assumptions; never fabricate).

## 9. Quality standards

- The bar every output must clear before it leaves this agent.
- Relevant [quality gates](../../handbook/governance/quality-gates.md) and [standards](../../handbook/standards/).

## 10. KPIs

- The measurable indicators of this agent's performance.
- Targets where applicable.

## 11. Review requirements

- Who (which agent) reviews this agent's output before acceptance.
- What the reviewer checks.
