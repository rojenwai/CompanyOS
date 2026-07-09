# Technology Readiness Levels (TRL)

TRL is a 1-9 scale that measures **how mature a technology is** - from a basic idea to a proven system
running in the real world. Originating at NASA and adopted by defense, aerospace, energy, biotech, and
government/EU grant programs (Horizon Europe and others require it), TRL gives everyone a shared, honest
language for the question deep-tech companies most often fudge: *how real is this technology, actually?*

> **TRL separates a promising lab result from a deployable product.** It turns "the tech works" into a
> specific, evidenced claim - which de-risks R&D spend and sets honest expectations with investors and
> partners. It is the [evidence-over-assumptions](principles.md) principle applied to technology maturity.

## The nine levels

| TRL | Name | What it means (the evidence that earns it) |
|---|---|---|
| **1** | Basic principles observed | The underlying science is observed and reported (a paper, an equation) |
| **2** | Technology concept formulated | A practical application is imagined; still no experimental proof |
| **3** | Experimental proof of concept | The key function is proven analytically or in the lab, in isolation |
| **4** | Validated in the lab | Components are integrated and work together under lab conditions |
| **5** | Validated in a relevant environment | The system works under realistic (not just lab) conditions |
| **6** | Demonstrated in a relevant environment | A full prototype/pilot runs in near-real conditions |
| **7** | Prototype in the operational environment | A near-final system is demonstrated in the actual environment |
| **8** | System complete and qualified | Final form, fully tested, and qualified/certified |
| **9** | Proven in the operational environment | Deployed and running in real production use |

## The three phases (and the valley of death)

```
TRL 1-3  RESEARCH      idea -> proof of concept        (owned by research/, ai/)
TRL 4-6  DEVELOPMENT   lab -> relevant environment     <-- the "valley of death"
TRL 7-9  DEPLOYMENT    operational -> production        (owned by engineering/, hardware/, post-launch/)
```

**The valley of death is TRL 4-6:** the technology is too mature for research grants but too immature for
product investment, and most deep tech dies there for lack of focus or funding. Plan and fund the crossing
**deliberately** - it is a strategic decision, not an afterthought ([strategy](../strategy/README.md)).

## How Company OS uses TRL

- **Assess honestly.** Research assigns a TRL to any novel technology and never inflates it - a TRL-3
  result described as "nearly a product" is a lie that wastes money later.
- **Gate investment by level.** Do not try to productize a TRL-3 technology, and do not keep
  over-researching a TRL-7 one. Match the effort (and the funding source) to the level.
- **Feed [opportunity scoring](opportunity-scoring.md).** A low TRL raises technical difficulty and risk;
  it is a direct input to feasibility when [ranking opportunities](../../../ai/agents/research/opportunity-ranking-agent.md).
- **Set expectations with investors.** A TRL-4 story is a *research bet*, not a *product* - pitch it as
  what it is ([pitching](../strategy/pitching.md), [finding investors](../strategy/finding-investors.md)).
- **De-risk one gate at a time.** Each level is a gate: name the specific evidence that would advance the
  technology to the next level, then go get exactly that.

## Where it connects across the OS

- **[Hardware](../hardware/README.md)** — physical products live and die on TRL; each level maps to
  design, prototype, and [test-plan gates](../hardware/quality-gates.md).
- **[AI](../ai-engineering/evaluation-and-testing.md)** — for novel models, tie TRL advancement to passing the
  evaluation suite in progressively more realistic conditions (offline → sim → shadow → production).
- **[Innovation Review Board](innovation-framework.md)** — TRL is the honest answer to the board's
  "*is it buildable?*" question.
- **[SDLC](../../workflows/sdlc.md)** — once a technology reaches ~TRL 7, it enters normal product
  development; the SDLC takes over from research.

## Related readiness frameworks

TRL has siblings worth knowing when the technology is novel:

- **MRL (Manufacturing Readiness Level)** — can it be *produced* at quality, volume, and cost? Critical
  for [hardware](../hardware/README.md); high TRL with low MRL still cannot ship.
- **CRL (Commercial Readiness)** — is the *market and business model* ready, independent of the tech?
- **IRL (Integration Readiness)** — how ready are the *interfaces* between components/systems?

## When to use TRL (and when not to)

Use it whenever the **core technology itself is unproven**: deep tech, hardware, robotics, drones,
embedded, novel AI, biotech, energy, and materials. Do **not** bother for a straightforward software
application built on proven technology - it effectively starts at TRL 7-9, and the
[SDLC](../../workflows/sdlc.md) plus normal [validation](../strategy/idea-validation.md) is enough. Using TRL
where it does not apply is just ceremony.
