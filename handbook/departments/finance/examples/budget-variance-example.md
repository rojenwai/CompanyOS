# Example - Budget vs. Actual Variance

> Worked example - illustrative, not a live record. Produced in the
> [monthly close](../checklists/monthly-close-checklist.md); every number traces to a source
> ([standards](../standards.md)).

**Period:** June 2026 · **Prepared by:** Financial Planning Agent · **Reviewed by:** CFO

## Summary

| Line | Budget | Actual | Variance | % |
|---|---|---|---|---|
| Revenue | $95,000 | $88,400 | **-$6,600** | -6.9% |
| Cloud infrastructure | $28,000 | $41,200 | **-$13,200** | -47.1% |
| AI / model costs | $12,000 | $9,100 | +$2,900 | +24.2% |
| Payroll | $210,000 | $210,000 | $0 | 0% |
| Marketing | $18,000 | $14,500 | +$3,500 | +19.4% |
| **Net burn** | **-$173,000** | **-$186,400** | **-$13,400** | -7.7% |

## Explanation of material variances

**Cloud infrastructure, -$13,200 (unfavourable).** A misconfigured autoscaling policy left a staging
cluster running at production capacity for 19 days. Detected by the cost alert on day 19 - too late.
*Root cause is process, not price.*

- **Action:** cost alert threshold lowered and now pages on 3-day trend, not month-total
  ([high-cloud-cost playbook](../../post-launch/playbooks/high-cloud-cost.md)).
- **Action:** staging environments now scale to zero outside working hours (owner: Platform Engineer, due 15 Jul).
- **Recovered:** ~$11k/month run-rate going forward.

**Revenue, -$6,600 (unfavourable).** Two enterprise deals slipped from June to July - both signed 3 July.
Not lost; timing only. Forecast reflects the shift; no change to the annual plan.

**AI costs, +$2,900 (favourable).** Prompt caching and right-sizing to a smaller model on the summarizer
path reduced cost per resolved task from $0.006 to $0.004 with no quality regression
([model card](../../ai-engineering/examples/model-card-example.md)).

## Runway impact

Net burn ran $13,400 over plan, driven almost entirely by the cloud incident. With that fixed, run-rate
burn returns to plan. Adjusted runway moves from 28 to **27.4 months** - well above the 12-month trigger
([runway model](runway-model-example.md)). **No action required beyond the fixes above.**

---

## Why this variance report works

It doesn't just report the number - it names the **root cause**, assigns an **owner and a date**, states
what was **recovered**, and separates a real problem (cloud) from a timing artefact (revenue). A variance
without a cause and an action is just an accounting entry.
