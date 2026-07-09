# Post-Launch Decision Frameworks

## Incident severity
Classify by customer impact and data/security risk ([incident-response](incident-response.md)); severity sets response speed and who is paged.

## Roll back vs. fix forward
- **Roll back** when a recent change caused the problem and a known-good state exists — the default for customer-impacting issues.
- **Fix forward** only when rollback is impossible (e.g. an irreversible migration) and the fix is fast and low-risk.

## Patch now vs. schedule
- **Now** — actively exploited security issues, data-integrity risks.
- **Scheduled** — non-urgent updates batched into the normal [maintenance](maintenance.md) cadence.

## Deprecate vs. maintain
Weigh usage, strategic value, and maintenance cost via [product evolution](product-evolution.md).

Irreversible actions require [approval](../../../ai/orchestration/approval-engine.md).
