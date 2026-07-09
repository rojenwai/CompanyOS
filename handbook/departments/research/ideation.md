# Ideation & Brainstorming

The earliest phase of a company - before problem discovery, before a line of code. The goal here is
**quantity and range**, not quality: generate a large pool of candidate ideas, then converge on the few
worth [validating](../strategy/idea-validation.md). Falling in love with your first idea is the most
common early mistake.

> **Diverge, then converge.** First generate wildly without judgment. Only afterward filter, cluster, and
> score. Mixing the two kills good ideas before they are born.

## Where good ideas actually come from

Ideas are rarely lightning bolts. They come from deliberately looking where others do not:

| Source | Prompt to ask |
|---|---|
| **Personal pain** | What do *you* repeatedly struggle with, hack around, or pay to avoid? |
| **Observed pain** | Where do you watch others waste time, money, or patience? |
| **Enabling shifts** | What just became possible (new AI capability, cheaper hardware, new API, regulation change)? |
| **Inefficiency & arbitrage** | Where is an industry slow, manual, expensive, or opaque for no good reason? |
| **First principles** | If you rebuilt this from scratch today, ignoring how it is done now, what would it look like? ([first-principles.md](first-principles.md)) |
| **Cross-pollination** | What works in industry A that no one has applied to industry B? |
| **Trend-riding** | What behavior or technology is growing fast, and what does it make newly necessary? |
| **Frustration mining** | Read support forums, app-store reviews, and complaint threads - documented pain at scale. |

## Techniques to generate range

- **10x, not 10%.** Ask what a dramatically better solution looks like, not a marginally better one.
- **Constraint relaxation.** "What if this were free / instant / legal everywhere / had unlimited compute?" Remove a constraint and see what opens up.
- **SCAMPER.** Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse an existing solution.
- **Inversion.** Instead of "how do we succeed?", ask "what would guarantee failure?" - then avoid it. (See [first principles](first-principles.md).)
- **Jobs-to-be-done.** What job is a customer "hiring" a product to do? What are they firing today?
- **Extreme users.** Design for the most demanding user; the mainstream often follows.

## How to run a brainstorm

1. **Frame a fertile question.** Broad enough for range, narrow enough for focus: "How might we remove the pain of X for Y?"
2. **Diverge (no judgment).** Quantity over quality; wild ideas welcome; build on others' ideas; defer all criticism. Aim for dozens.
3. **Cluster.** Group the raw ideas into themes.
4. **Converge.** Score the strongest with [opportunity-scoring](opportunity-scoring.md) (problem severity, frequency, feasibility, defensibility, market, timing).
5. **Shortlist.** Pick the top few to run through [idea validation](../strategy/idea-validation.md) - never build straight from a brainstorm.

## Anti-patterns

- **Solution-first.** Starting with "I want to build X" instead of "who has what painful problem." Start with the problem.
- **Falling in love early.** Committing before validation. Ideas are cheap; conviction should be earned.
- **Brainstorming only alone.** Diverse inputs produce range; solo ideation narrows fast.
- **Confusing novelty with value.** A clever idea nobody needs is worthless. Significance beats cleverness ([research principles](principles.md)).

## Output

A shortlist of 3-5 candidate ideas, each framed as a *problem* with a hypothesis, handed to
[idea validation](../strategy/idea-validation.md) and scored by the
[Opportunity Ranking Agent](../../../ai/agents/research/opportunity-ranking-agent.md). This is Stage 0 of the
[startup lifecycle](../strategy/startup-lifecycle.md).
