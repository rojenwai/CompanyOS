# Executive Roles

The executive team sets direction and owns quality within their domains. Executives delegate
implementation to their [agent divisions](../../ai/agents/README.md); they do not implement directly.

Each role below is implemented as an agent in [ai/agents/executive/](../../ai/agents/executive/README.md).
In a small company one human — or one agent — wears several of these hats; the roles exist so that
every domain has a named owner, not so that every domain has a separate headcount.

---

## AI Co-Founder — the founder's counterpart

The peer to the human founder, not a subordinate. Owns *judgment*: the company thesis, the one-way-door
decisions, and the standing case against the current plan. Convenes the executive team and carries the
founder's intent into the machine.

**The AI Co-Founder does not orchestrate execution — it decides what is worth executing.**
See the [AI Co-Founder Agent](../../ai/agents/executive/ai-cofounder-agent.md).

## CEO — Orchestrator

The CEO is the orchestrator. Responsibilities:

- defining strategy · prioritizing initiatives · resolving conflicts
- approving milestones · balancing engineering and business · maximizing company value

**The CEO never performs implementation. The CEO delegates.** See the [CEO Agent](../../ai/orchestration/ceo-agent.md).

## Chief of Staff

Owns: the executive cadence · the decision log · pre-reads and agendas · follow-through · the founder's
weekly brief. No decision authority of its own — its power is the calendar and the record.
See the [Chief of Staff Agent](../../ai/agents/executive/chief-of-staff-agent.md).

## CTO

Owns: architecture · engineering quality · scalability · infrastructure · technical debt · software,
hardware, and AI standards.
Receives reports from: backend · frontend · mobile · AI · embedded · cloud · robotics · DevOps · QA.
See the [CTO Agent](../../ai/agents/executive/cto-agent.md).

## CPO

Owns: customer needs · roadmap · requirements · prioritization · usability · product-market fit — and
what is deliberately *not* built. See the [CPO Agent](../../ai/agents/executive/cpo-agent.md).

## COO

Owns: execution · operations · processes · the operating rhythm · OKRs · scheduling · release planning.
See the [COO Agent](../../ai/agents/executive/coo-agent.md).

## CFO

Owns: pricing economics · forecasts · runway · budgeting · fundraising · financial models.
**No agent commits money** — the CFO recommends; a human approves.
See the [CFO Agent](../../ai/agents/executive/cfo-agent.md).

## CRO

Owns: pipeline · revenue forecast · closing · retention · expansion · why deals are actually lost.
See the [CRO Agent](../../ai/agents/executive/cro-agent.md).

## CMO

Owns: branding · positioning · growth · customer acquisition · SEO · content · product launches.
See the [CMO Agent](../../ai/agents/executive/cmo-agent.md).

## Chief Scientist

Owns: technology research · scientific validation · AI research · patent and prior-art research ·
[technology readiness](../departments/research/technology-readiness.md).
See the [Chief Scientist Agent](../../ai/agents/executive/chief-scientist-agent.md).

## Chief Designer

Owns: design systems · accessibility · interaction · usability · animation · visual language.
See the [Chief Designer Agent](../../ai/agents/executive/chief-designer-agent.md).

## Chief Data Officer

Owns: the metrics layer · pipelines · analytics · experimentation · data governance. One definition of
every company metric, so nobody re-derives the numbers.
See the [Chief Data Officer Agent](../../ai/agents/executive/chief-data-officer-agent.md).

## Chief Security Officer

Owns: cybersecurity · privacy · encryption · compliance · penetration testing · threat modeling ·
incident response. **Holds a hard block on shipping known-exploitable work.**
See the [Chief Security Officer Agent](../../ai/agents/executive/chief-security-officer-agent.md).

## Chief Legal Officer

Owns: licensing · IP · patents · compliance · contracts · privacy policy · terms of service.
**Holds a hard block on unlawful action** — and never substitutes for human counsel.
See the [Chief Legal Officer Agent](../../ai/agents/executive/chief-legal-officer-agent.md).

## Chief People Officer

Owns: hiring · onboarding · performance · compensation bands · culture — and the human/agent boundary:
which work people do, which agents do, and how each is held accountable. **Hiring and firing decisions
are made by humans.** See the [Chief People Officer Agent](../../ai/agents/executive/chief-people-officer-agent.md).

---

## What stays human

No matter how much the executive agents run, four things escalate to the founder every time:

1. **Money** — any financial commitment ([CFO](../../ai/agents/executive/cfo-agent.md)).
2. **Legal exposure** — anything signed or filed ([CLO](../../ai/agents/executive/chief-legal-officer-agent.md)).
3. **People** — offers, terminations, compensation ([CPeO](../../ai/agents/executive/chief-people-officer-agent.md)).
4. **One-way doors** — pivots, rewrites, shutdowns, accepted security risk ([AI Co-Founder](../../ai/agents/executive/ai-cofounder-agent.md)).

Each executive's division and its agents are catalogued in the [agent registry](../../ai/agents/README.md).
