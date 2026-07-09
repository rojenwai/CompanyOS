# Decision Memory

**Scope:** significant decisions across the company, long-lived.

## What's stored
Each decision, its rationale, the alternatives considered, who approved it, and the date — so decisions are traceable and not repeatedly reopened.

## Lifetime
Permanent and append-only.

## Writers / readers
Written by the [CEO Agent](../orchestration/ceo-agent.md), [Approval Engine](../orchestration/approval-engine.md), and meeting flows; read by the decision framework to check for prior art.

## Format
Follows the [decision framework](../../handbook/governance/decision-framework.md); architectural decisions use [ADRs](../../handbook/templates/documents/adr.md).
