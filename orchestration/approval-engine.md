# Approval Engine

The approval engine applies [governance](../governance/) to work that has passed review, deciding
whether it can proceed autonomously or requires human sign-off.

## What it enforces

- The [quality gates](../governance/quality-gates.md) for the current phase.
- The reversible/irreversible test from the [decision framework](../governance/decision-framework.md).
- **Human-in-the-Loop (HITL)** for high-risk actions.

## Human-in-the-Loop is mandatory for

- Financial commitments
- Legal documents
- Production deployments
- Security-sensitive actions
- Irreversible operations
- Customer-impacting changes

## Flow

```
Reviewed deliverable
  │
  ▼
Gates satisfied? ──no──► return to author (via Coordinator)
  │ yes
  ▼
Irreversible or high-risk? ──yes──► request human approval ──► approved? ──no──► hold/rework
  │ no                                                          │ yes
  ▼                                                             ▼
Autonomous approval ──────────────────────────────────► Execution Engine
```

A [Security Reviewer](security-reviewer.md) **Block** cannot be auto-approved — it always requires
explicit human override. All approvals are recorded to [decision memory](../memory/decision-memory.md).
