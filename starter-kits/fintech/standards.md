# Fintech - Added Standards

These extend the core [standards](../../handbook/standards/README.md) with what this company type specifically requires.

1. **Regulatory permission precedes launch.** Determine licensing (or a licensed partner) before building far - [legal](../../handbook/departments/legal/README.md) owns the gate.
2. **The ledger is double-entry, immutable, and reconciled daily.** Money must always balance; never mutate a posted entry.
3. **Never store raw card data or credentials.** Tokenize; comply with PCI-DSS ([security standards](../../handbook/departments/engineering/security-standards.md)).
4. **KYC/AML checks are enforced in the product**, not bolted on - with sanctions screening and suspicious-activity reporting.
5. **Every money-moving action is idempotent, audited, and reversible** where the law requires.
6. **Fraud and transaction monitoring run in real time**, with alerting to on-call ([monitoring](../../handbook/departments/post-launch/monitoring.md)).
