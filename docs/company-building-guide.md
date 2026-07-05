# The Company-Building Guide

> The single front-to-back guide to **what you need to learn** and **what you actually do** to build
> and run a company on [Company OS](../README.md). Every step links to the part of the OS that does the
> work — so this guide is both a syllabus and a map.

**You do not have to master everything.** A founder needs *working literacy* across all functions and
*depth* in one or two. Everything else is delegated — to hires or to the [AI agent workforce](../agents/README.md).
This guide tells you what "working literacy" means for each area and where the OS carries the load.

- **Part A — Skills to learn** (the syllabus)
- **Part B — Steps to build a company** (zero → launch → scale)
- **Part C — Steps to manage a company** (the ongoing operating rhythm)
- **Part D — What kills companies** (avoidable mistakes)

---

## Part A — Skills to learn

Legend for **depth**: 🟢 Working literacy (know enough to make decisions & hire) · 🔵 Go deep (a founder edge).

### 1. Foundational / meta skills — 🔵 everyone
The skills under every other skill.

| Skill | Why it matters | Learn by |
|---|---|---|
| First-principles thinking | Avoid copying; find better solutions | [research/first-principles.md](../research/first-principles.md) |
| Decision-making under uncertainty | Most founder work is deciding with incomplete data | [governance/decision-framework.md](../governance/decision-framework.md) |
| Evidence over assumption | Kills expensive guesses early | [company/principles.md](../company/principles.md) |
| Clear written communication | Reports, PRDs, pitches, hiring — all writing | [governance/communication-rules.md](../governance/communication-rules.md) |
| Systems thinking & prioritization | Spend limited time on the highest-leverage thing | [product/decision-frameworks.md](../product/decision-frameworks.md) |
| Learning how to learn | You will enter ten fields you don't know | [research/research-framework.md](../research/research-framework.md) |

### 2. Leadership & management — 🔵 founder/CEO
| Skill | Why | Where in OS |
|---|---|---|
| Setting vision & strategy | Aligns everyone on where and why | [company/vision.md](../company/vision.md) · [product/vision.md](../product/vision.md) |
| Delegation & orchestration | The CEO delegates, never implements | [orchestration/ceo-agent.md](../orchestration/ceo-agent.md) |
| Hiring & team building | Your #1 multiplier | see Part C, and `hr/` (planned) |
| Running a cadence (meetings, reviews) | Turns strategy into execution | [templates/documents/meeting-notes.md](../templates/documents/meeting-notes.md) |
| Conflict resolution | Cross-functional friction is constant | [orchestration/execution-lifecycle.md](../orchestration/execution-lifecycle.md) |

### 3. Product — 🔵 (most important single skill for a tech founder)
| Skill | Why | Where |
|---|---|---|
| Customer discovery & JTBD | Build the right thing | [product/discovery.md](../product/discovery.md) |
| Writing requirements (PRDs, stories) | Unambiguous build instructions | [product/requirements.md](../product/requirements.md) |
| Prioritization (RICE/MoSCoW/Kano) | Say no to 90% | [product/decision-frameworks.md](../product/decision-frameworks.md) |
| Defining an MVP | Ship the smallest useful thing | [agents/product/mvp-planning-agent.md](../agents/product/mvp-planning-agent.md) |
| Metrics & product-market fit | Know if it's working | [product/metrics.md](../product/metrics.md) |

### 4. Engineering / technical — 🟢–🔵 (deep if you're the technical founder)
| Skill | Why | Where |
|---|---|---|
| Architecture & trade-offs | Foundational decisions are expensive to reverse | [engineering/organization.md](../engineering/organization.md) · [templates/documents/adr.md](../templates/documents/adr.md) |
| Coding standards & review | Quality that lasts | [engineering/standards.md](../engineering/standards.md) · [engineering/review-process.md](../engineering/review-process.md) |
| Testing discipline | Ship without fear | [engineering/testing-standards.md](../engineering/testing-standards.md) |
| Delivery (git, CI/CD, releases) | Ship safely and often | [engineering/workflows.md](../engineering/workflows.md) |
| The full lifecycle | No phase skipped | [workflows/sdlc.md](../workflows/sdlc.md) |

### 5. AI / ML — 🟢–🔵 (deep for an AI-native company)
| Skill | Why | Where |
|---|---|---|
| AI as engineering (not prompt-writing) | Reliability, not demos | [ai/README.md](../ai/README.md) |
| RAG & grounding | Accuracy over hallucination | [ai/README.md](../ai/README.md#retrieval-augmented-generation-rag) |
| Evaluation & testing | Prove the model is good | [ai/evaluation-and-testing.md](../ai/evaluation-and-testing.md) |
| Cost & model selection | Margins depend on it | [ai/README.md](../ai/README.md#cost-optimization) |
| AI security | Prompt injection, data leakage | [ai/ai-security.md](../ai/ai-security.md) |

### 6. Design — 🟢
UX research, information architecture, the design system, accessibility, interaction design →
[design/README.md](../design/README.md). *Why:* usability and trust are product features.

### 7. Research & innovation — 🟢
Market/technical/scientific/patent research, opportunity scoring, competitive intelligence →
[research/README.md](../research/README.md). *Why:* it answers "what should we build next?"

### 8. Business & strategy — 🔵 founder
| Skill | Why | Where |
|---|---|---|
| Market sizing (TAM/SAM/SOM) | Is this big enough? | [strategy/market-analysis.md](../strategy/market-analysis.md) |
| Business models & pricing | How you make money | [strategy/business-model.md](../strategy/business-model.md) |
| Competitive analysis (SWOT/Porter/PESTLE) | Where you win | [strategy/market-analysis.md](../strategy/market-analysis.md) |
| Unit economics (CAC/LTV) | Whether the business works | [strategy/unit-economics.md](../strategy/unit-economics.md) |

### 9. Finance — 🟢 (hire depth early)
Forecasting, runway, budgeting, fundraising, financial models → [strategy/unit-economics.md](../strategy/unit-economics.md).
*Why:* running out of cash is the #1 killer. Know your runway to the week.

### 10. Marketing & growth — 🟢
Positioning, messaging, SEO/content, growth channels, launches → [strategy/go-to-market.md](../strategy/go-to-market.md).
*Why:* a great product no one hears about fails.

### 11. Sales — 🟢–🔵 (founder sells first)
The [selling method](../sales/methodology.md) (qualify → discover → value → close), [buyer psychology](../sales/psychology.md), and [where to sell](../sales/channels.md) → [sales/](../sales/README.md).
*Why:* founders must close the first ~100 customers themselves.

### 12. Legal & compliance — 🟢 (hire depth)
Incorporation, IP/patents/trademarks, contracts, privacy (GDPR), terms, open-source licensing,
data-protection → owned by the [Chief Legal Officer](../company/roles.md). *Why:* mistakes here are expensive and slow to fix.

### 13. Operations & people (HR) — 🟢
Hiring, onboarding, meetings, project management, vendor & asset management, culture →
[operations/](../operations/README.md) and [hr/](../hr/README.md). *Why:* the company is the product too.

### 14. Security — 🟢 (hire depth)
Threat modeling, encryption, auth, compliance, incident readiness → [engineering/security-standards.md](../engineering/security-standards.md)
· [ai/ai-security.md](../ai/ai-security.md). *Why:* one breach can end a company's trust.

### 15. Customer success & support — 🟢
Onboarding, health scoring, churn/renewal, feedback loops → [post-launch/support.md](../post-launch/support.md).
*Why:* retention beats acquisition; keeping customers compounds.

### 16. Founder personal skills — 🔵
Resilience, time management, energy management, saying no, fundraising storytelling, and knowing when to
delegate. *Why:* the founder is the constraint most often.

> **How to learn any of these fast:** run the [research workflow](../research/research-framework.md) —
> define a sharp question, gather multiple sources, organize, form a hypothesis, then *do* the thing and
> validate. Learning-by-shipping beats learning-by-reading.

---

## Part B — Steps to build a company

The end-to-end journey from an idea to a scaling business. Each step names the **outcome**, the
**actions**, and the **OS home** where the work lives. This is the [SDLC](../workflows/sdlc.md) and the
[startup lifecycle](../strategy/startup-lifecycle.md) told as a founder's to-do list.

### Step 0 — Prepare yourself
**Outcome:** enough literacy and the right mindset. **Do:** skim Part A; adopt the [core principles](../company/principles.md); accept that you'll delegate most execution to hires and [agents](../agents/README.md).

### Step 1 — Generate & find a real problem
**Outcome:** a shortlist of problem-framed ideas, then one validated, painful, worth-years problem. **Do:** [brainstorm ideas](../research/ideation.md) (diverge then converge), then run [problem discovery](../product/discovery.md); score with the [problem-evaluation criteria](../strategy/startup-lifecycle.md). **Gate:** problem validated with evidence.

### Step 2 — Research the space
**Outcome:** you understand the market, competitors, and technical feasibility. **Do:** [research framework](../research/research-framework.md); [competitive analysis](../strategy/market-analysis.md). **Gate:** opportunity confirmed.

### Step 3 — Validate demand
**Outcome:** proof people want this and will pay. **Do:** climb the [validation ladder](../strategy/idea-validation.md) - interviews, landing pages, fake doors, pre-sales; size [TAM/SAM/SOM](../strategy/market-analysis.md). **Gate:** clear demand identified (real signals, not compliments).

### Step 4 — Choose a business model
**Outcome:** how you create and capture value. **Do:** pick a [model & pricing](../strategy/business-model.md); sanity-check [unit economics](../strategy/unit-economics.md). **Gate:** viable model.

### Step 5 — Handle the legal foundation
**Outcome:** a real company you can operate safely. **Do:** incorporate; found­ers' agreements & equity; IP assignment; bank account; basic contracts, privacy policy & terms (Chief Legal Officer scope → [company/roles.md](../company/roles.md)). **Gate:** legally able to hire, sell, and raise.

### Step 6 — Stand up Company OS & the team
**Outcome:** an operating system and the people/agents to run it. **Do:** adopt [company](../company/README.md) + [governance](../governance/README.md) + the [kernel](../orchestration/README.md); activate the [agents](../agents/README.md) you need; hire your first critical roles. **Gate:** work can be routed, reviewed, and shipped.

### Step 7 — Define the product
**Outcome:** a clear, prioritized plan. **Do:** [product definition](../product/README.md); write the [PRD](../product/requirements.md); scope the [MVP](../agents/product/mvp-planning-agent.md). **Gate:** requirements ready; stories at [Definition of Ready](../engineering/definition-of-ready.md).

### Step 8 — Design & build the MVP
**Outcome:** the smallest useful product. **Do:** [design](../design/README.md) → [architecture](../engineering/organization.md) → build through the [SDLC](../workflows/sdlc.md) with [tests](../engineering/testing-standards.md) and [security review](../engineering/security-standards.md). Follow the [build-an-MVP playbook](../playbooks/building-an-mvp.md). **Gate:** [Definition of Done](../engineering/quality-gates.md).

### Step 9 — Launch
**Outcome:** the product is live with a safety net. **Do:** the [launch playbook](../playbooks/launching-a-product.md) — pass the [launch checklist](../product/quality-gates.md), wire [monitoring](../post-launch/monitoring.md), prepare [rollback](../post-launch/rollback.md). **Gate:** launched, instrumented, reversible.

### Step 10 — Get customers (go-to-market)
**Outcome:** a repeatable way to acquire users. **Do:** [GTM](../strategy/go-to-market.md); pick a [channel & sales motion](../sales/channels.md); sell founder-led for the first ~100 using the [sales method](../sales/methodology.md) and honest [buyer psychology](../sales/psychology.md). **Gate:** a channel that reliably brings customers at viable CAC.

### Step 11 — Reach product-market fit
**Outcome:** evidence the market pulls the product. **Do:** measure the [PMF indicators](../product/metrics.md); iterate via the [continuous improvement loop](../post-launch/continuous-improvement.md). **Gate:** strong retention + organic pull.

### Step 12 — Raise capital (if needed)
**Outcome:** funded runway to scale. **Do:** [find the right investors](../strategy/finding-investors.md) for your stage; [pitch](../strategy/pitching.md) the story; prepare the [fundraising pack](../strategy/unit-economics.md) and know your numbers; run the [fundraising playbook](../playbooks/fundraising.md). **Gate:** funded — or a profitable path without it.

### Step 13 — Scale
**Outcome:** growth without breaking. **Do:** scale [people, process, infra, automation](../strategy/unit-economics.md) only after repeatable sales and healthy [unit economics](../strategy/unit-economics.md). **Gate:** growth with stable reliability & margins.

### Step 14 — Expand & lead the category
**Outcome:** durable advantage. **Do:** [international expansion](../strategy/unit-economics.md); build moats toward [category leadership](../strategy/README.md). **Gate:** the default choice in your market.

---

## Part C — Steps to manage a company (the operating rhythm)

Building is finite; managing is forever. Management is a set of **cadences** that keep the company
healthy. Run these continuously.

### The rhythm
| Cadence | You do | OS home |
|---|---|---|
| **Daily** | Watch health/incidents; unblock people | [post-launch/monitoring.md](../post-launch/monitoring.md) · [on-call](../post-launch/on-call.md) |
| **Weekly** | Team syncs; metrics review; unblock; ship | [templates/documents/status-report.md](../templates/documents/status-report.md) |
| **Per sprint** | Plan → build → review → retro; repay [tech debt](../post-launch/technical-debt/repayment-plan.md) | [engineering/workflows.md](../engineering/workflows.md) |
| **Per release** | [Launch playbook](../playbooks/launching-a-product.md) + [continuous improvement](../post-launch/continuous-improvement.md) | [post-launch/release-management.md](../post-launch/release-management.md) |
| **Monthly** | Financials & runway; hiring; customer health | [strategy/unit-economics.md](../strategy/unit-economics.md) · [post-launch/support.md](../post-launch/support.md) |
| **Quarterly** | Strategy & roadmap review; OKRs; [product evolution](../post-launch/product-evolution.md) | [product/roadmap.md](../product/roadmap.md) |
| **Annually** | Vision refresh; budget; category strategy | [company/vision.md](../company/vision.md) · [strategy/README.md](../strategy/README.md) |

### The management surfaces you own
- **People** — hire, onboard, grow, and retain (culture, roles, feedback).
- **Money** — runway, budget, unit economics, fundraising ([finance](../strategy/unit-economics.md)).
- **Customers** — success, retention, feedback → roadmap ([post-launch/support.md](../post-launch/support.md), [customer-feedback.md](../post-launch/customer-feedback.md)).
- **Product** — direction, prioritization, PMF, evolution ([product/](../product/README.md)).
- **Reliability** — uptime, incidents, maintenance, security ([post-launch/](../post-launch/README.md)).
- **Risk** — legal, security, compliance, and [decision governance](../governance/README.md).

### Manage by delegation
The CEO's job is to **orchestrate, not execute** ([ceo-agent.md](../orchestration/ceo-agent.md)). Route
work to the right [division](../agents/README.md), let [reviewers](../orchestration/reviewer.md) gate
quality, keep [Human-in-the-Loop](../orchestration/approval-engine.md) for high-risk calls, and capture
every lesson to [memory](../memory/lessons-learned.md) so the company compounds.

---

## Part D — What kills companies (and the antidote)

| Failure | Antidote in Company OS |
|---|---|
| Building something nobody wants | [Discovery](../product/discovery.md) & demand validation **before** building |
| Running out of cash | Weekly runway tracking; [unit economics](../strategy/unit-economics.md) |
| No focus (building everything) | Ruthless [prioritization](../product/decision-frameworks.md) & [MVP](../agents/product/mvp-planning-agent.md) |
| Shipping unreliable software | [Quality gates](../governance/quality-gates.md), [testing](../engineering/testing-standards.md), [reviews](../engineering/review-process.md) |
| No one hears about it | [Go-to-market](../strategy/go-to-market.md) from day one |
| Churn eats growth | [Customer success](../post-launch/support.md) & retention focus |
| Founder burnout | Delegate to hires & [agents](../agents/README.md); own only what only you can |
| Repeating mistakes | [Lessons learned](../memory/lessons-learned.md) + [continuous improvement](../post-launch/continuous-improvement.md) |
| Security/legal blowups | [Security](../engineering/security-standards.md) & [legal](../company/roles.md) as gates, not afterthoughts |

---

**Where to go next:** the [Company OS hub](../README.md) · the [SDLC](../workflows/sdlc.md) ·
the [startup lifecycle](../strategy/startup-lifecycle.md). This guide is the trailhead; the departments
do the work.
