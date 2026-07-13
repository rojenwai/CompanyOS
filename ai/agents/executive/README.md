# Executive Division — the C-Suite

The executive layer sits between the human founder and the twenty specialist divisions. Executives
**set direction and own quality** in their domain; they delegate implementation and never do it
themselves. Each one is the accountable owner of the departments listed below — which is what makes
"**Reports to:** CTO" on a specialist agent spec mean something concrete.

Every spec follows the [standard 11-section format](../agent-template.md). The executive roles they
implement are described for humans in [handbook/company/roles.md](../../../handbook/company/roles.md).

## Chain of command

```
Human Founder                      one-way doors, money, legal, people — always human
│
└── AI Co-Founder                  direction & judgment: the thesis, the hard calls, the dissent
    │
    └── CEO Agent (kernel)         orchestration: objective → plan → routed work → review → ship
        │
        ├── Chief of Staff         the decision log and the follow-through
        │
        ├── CTO                    Engineering · DevOps · AI · Hardware · Post-Launch
        ├── CPO                    Product · Documentation
        ├── Chief Designer         Design
        ├── Chief Scientist        Research
        ├── COO                    Operations
        ├── CFO                    Finance · Investor Relations
        ├── CRO                    Sales · Customer Success
        ├── CMO                    Marketing
        ├── CDO                    Data
        ├── CSO                    Security
        ├── CLO                    Legal
        └── CPeO                   HR / People
```

**AI Co-Founder vs. CEO Agent** — the two are deliberately different jobs. The
[AI Co-Founder](ai-cofounder-agent.md) owns *whether the company is doing the right thing*: the
thesis, the one-way doors, and the standing argument against the current plan. The
[CEO Agent](../../orchestration/ceo-agent.md) is the [kernel](../../orchestration/README.md) — it owns
*getting the agreed thing done*: objectives into plans, plans into routed work, work into reviewed,
approved, shipped output. If you only keep one, keep the CEO Agent; the Co-Founder is the one you
want when the question is "should we be building this at all?"

## Roster

| Agent | Owns | Supervises |
|---|---|---|
| [AI Co-Founder](ai-cofounder-agent.md) | Thesis · strategy · one-way doors · the honest read on whether it's working | the executive team |
| [CEO Agent](../../orchestration/ceo-agent.md) ↗ | Orchestration: objectives, prioritization, conflict resolution, milestones | every division (spec lives in the [kernel](../../orchestration/README.md)) |
| [Chief of Staff](chief-of-staff-agent.md) | The decision log · executive cadence · follow-through | — |
| [CTO](cto-agent.md) | Architecture · engineering quality · scalability · technical debt | [engineering](../engineering/) · [devops](../devops/) · [ai](../ai-engineering/) · [hardware](../hardware/) · [post-launch](../post-launch/) |
| [CPO](cpo-agent.md) | Roadmap · requirements · prioritization · product-market fit | [product](../product/) · [documentation](../documentation/) |
| [Chief Designer](chief-designer-agent.md) | Design system · interaction · accessibility · craft | [design](../design/) |
| [Chief Scientist](chief-scientist-agent.md) | Research agenda · scientific validation · [TRL](../../../handbook/departments/research/technology-readiness.md) · prior art | [research](../research/) |
| [COO](coo-agent.md) | Execution · operating rhythm · OKRs · process · vendors | [operations](../operations/) |
| [CFO](cfo-agent.md) | Model · forecast · runway · budget · unit economics | [finance](../finance/) · [investor-relations](../investor-relations/) |
| [CRO](cro-agent.md) | Pipeline · forecast · retention · expansion | [sales](../sales/) · [customer-success](../customer-success/) |
| [CMO](cmo-agent.md) | Positioning · brand · growth · launches | [marketing](../marketing/) |
| [CDO](chief-data-officer-agent.md) | The metrics layer · analytics · experimentation · governance | [data](../data/) |
| [CSO](chief-security-officer-agent.md) | Threat model · privacy · compliance · incident response | [security](../security/) |
| [CLO](chief-legal-officer-agent.md) | Contracts · IP · licensing · terms | [legal](../legal/) |
| [CPeO](chief-people-officer-agent.md) | Hiring · onboarding · performance · culture · the human/agent boundary | [hr](../hr/) |

[strategy](../strategy/) reports to the [AI Co-Founder](ai-cofounder-agent.md) directly — it is the
division that does the thinking the Co-Founder is accountable for.

## The three hard blocks

Most executive disagreements are resolved by the [CEO Agent](../../orchestration/ceo-agent.md). Three
are not, and no agent may override them — only the human founder, in writing, with the risk stated:

1. **[CSO](chief-security-officer-agent.md)** — known-exploitable work does not ship.
2. **[CLO](chief-legal-officer-agent.md)** — unlawful or uninsurable action does not proceed.
3. **[CFO](cfo-agent.md)** — no agent commits money.

## Customizing

You almost certainly do not need fourteen executives. A two-person company needs the
[AI Co-Founder](ai-cofounder-agent.md), the [CEO Agent](../../orchestration/ceo-agent.md), a
[CTO](cto-agent.md), and a [CPO](cpo-agent.md) — the other roles are being done by the founder
whether or not there is a file for them. Add an executive when the domain has become bigger than the
founder's attention, and delete the specs you have not activated. When you delete one, re-point the
**Reports to:** line of the agents beneath it, then run `python scripts/check-links.py`.
