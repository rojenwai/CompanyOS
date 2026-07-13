# Company Structure

The AI organization operates exactly like a technology company.

```
Human Founder
│
└── AI Co-Founder            direction & judgment; the one-way doors stay human
    │
    └── CEO                  the orchestrator: objectives, priorities, milestones
        │
        ├── Chief of Staff   the decision log and the follow-through
        │
        ├── CTO              ├── CFO
        ├── CPO              ├── CRO
        ├── COO              ├── CMO
        ├── Chief Designer   ├── Chief Data Officer
        ├── Chief Scientist  ├── Chief Security Officer
        ├── Chief People Officer └── Chief Legal Officer
```

Each executive supervises specialized agents. See [roles.md](roles.md) for each executive's mandate,
[ai/agents/executive/](../../ai/agents/executive/README.md) for the executive agent specs, and
[agents/](../../ai/agents/) for the workforce beneath them.

---

## Organizational rules

Every department:

1. reviews work
2. challenges assumptions
3. proposes improvements
4. estimates risk
5. documents decisions

**No department works in isolation. Cross-functional collaboration is mandatory.**

Strategic work requires cross-functional review before approval by the CEO (see the
[governance decision framework](../governance/decision-framework.md)).

## From executives to agents

Each executive maps to one or more agent divisions in the [AI organization](../../ai/agents/README.md):

| Executive | Owns these divisions |
|---|---|
| [AI Co-Founder](../../ai/agents/executive/ai-cofounder-agent.md) | Strategy — and the standing argument against the current plan |
| [CTO](../../ai/agents/executive/cto-agent.md) | Engineering · DevOps · AI · Hardware · Post-Launch |
| [CPO](../../ai/agents/executive/cpo-agent.md) | Product · Documentation |
| [Chief Designer](../../ai/agents/executive/chief-designer-agent.md) | Design |
| [Chief Scientist](../../ai/agents/executive/chief-scientist-agent.md) | Research |
| [COO](../../ai/agents/executive/coo-agent.md) | Operations |
| [CFO](../../ai/agents/executive/cfo-agent.md) | Finance · Investor Relations |
| [CRO](../../ai/agents/executive/cro-agent.md) | Sales · Customer Success |
| [CMO](../../ai/agents/executive/cmo-agent.md) | Marketing |
| [Chief Data Officer](../../ai/agents/executive/chief-data-officer-agent.md) | Data |
| [Chief Security Officer](../../ai/agents/executive/chief-security-officer-agent.md) | Security |
| [Chief Legal Officer](../../ai/agents/executive/chief-legal-officer-agent.md) | Legal |
| [Chief People Officer](../../ai/agents/executive/chief-people-officer-agent.md) | HR / People |

The [orchestration kernel](../../ai/orchestration/) coordinates work across them.
