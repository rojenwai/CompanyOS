# Worked Example: One Company, End to End

> An illustrative walkthrough of a fictional company built on Company OS - to show how the pieces connect.
> It is a narrative, not a live record. The company: **PostmortemAI**, an [AI startup](../starter-kits/ai-startup/README.md)
> that auto-writes incident postmortems for SaaS engineering teams.

## The journey, mapped to the OS

| Step | What PostmortemAI did | OS home |
|---|---|---|
| **0. Prepare** | Founder adopted the core principles and the delegate-don't-implement model | [company/](../company/README.md), [ceo-agent](../orchestration/ceo-agent.md) |
| **1. Find a problem** | Found that teams waste 3-4 hrs/incident on postmortems and often skip them | [research](../research/README.md), [discovery](../product/discovery.md) |
| **2. Score it** | Scored the opportunity 6.9/10 → pursue | [opportunity score](../research/examples/opportunity-score-example.md) |
| **3. Business model** | Per-seat SaaS + usage add-on; LTV/CAC 12x | [business model example](../strategy/examples/business-model-example.md) |
| **4. Legal foundation** | Incorporated; IP assigned; standard terms + DPA | [legal](../legal/README.md) |
| **5. Stand up the OS** | Activated the [AI division](../starter-kits/ai-startup/agents.md), engineering, and product | [ai-startup kit](../starter-kits/ai-startup/README.md) |
| **6. Define the product** | Wrote a lean PRD; scoped the MVP to one job: accurate postmortems from telemetry | [prd](../templates/documents/prd.md), [MVP planning](../agents/product/mvp-planning-agent.md) |
| **7. Set the eval bar** | Defined "good" *before* building: <2% hallucination, >90% accepted | [ai evaluation](../ai/evaluation-and-testing.md) |
| **8. Build the MVP** | RAG-grounded on the customer's logs/traces; versioned prompts | [build-an-MVP playbook](../playbooks/building-an-mvp.md), [model card](../ai/examples/model-card-example.md) |
| **9. Launch** | Passed the launch checklist; monitoring + rollback ready | [launch playbook](../playbooks/launching-a-product.md) |
| **10. Get customers** | Founder-led sales; discovery-led deals; security review for enterprise | [sales](../sales/examples/discovery-notes-example.md), [enterprise kit](../starter-kits/enterprise-b2b/README.md) |
| **11. Reach PMF** | Strong retention + organic referrals; measured the PMF indicators | [product metrics](../product/metrics.md) |
| **12. Operate** | Weekly cadence; monthly runway; health scoring on every account | [operating rhythm](company-building-guide.md), [customer health](../customer-success/examples/health-score-example.md) |
| **13. Handle incidents** | A latency spike → blameless postmortem, action items tracked | [postmortem example](../post-launch/examples/postmortem-example.md) |
| **14. Improve & scale** | Telemetry + feedback → roadmap → scale after healthy unit economics | [continuous improvement](../post-launch/continuous-improvement.md), [scaling readiness](../strategy/checklists/scaling-readiness-checklist.md) |

## The point

No step was invented ad hoc - each one had a home in the OS, a standard to meet, and a gate to pass. That
is the value of an operating system: the founder made decisions and set direction; the
[departments](../STRUCTURE.md) and [agents](../agents/README.md) carried the load, and nothing fell
through the cracks. Start your own journey from the [Company-Building Guide](company-building-guide.md).
