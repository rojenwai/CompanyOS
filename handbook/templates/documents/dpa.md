# Data Processing Agreement (DPA) — <Controller> & <Processor>

> ⚠️ **Structural checklist, not legal advice.** A DPA is required whenever one party processes personal
> data on another's behalf (GDPR Art. 28 and equivalents). It must be reviewed by counsel
> ([legal](../../departments/legal/README.md)) and is typically an annex to the
> [MSA](sales-proposal.md) or vendor contract. Signature requires
> [human approval](../../../ai/orchestration/approval-engine.md).

## 1. Roles and scope

| Field | Value |
|---|---|
| Controller | <who determines purposes and means> |
| Processor | <who processes on the controller's behalf> |
| Subject matter | <what the processing is for> |
| Duration | <term, tied to the main agreement> |
| Nature & purpose | <e.g. hosting, analytics, support> |
| Categories of data | <e.g. contact details, usage data — never more than necessary> |
| Categories of data subjects | <e.g. customer employees, end users> |

## 2. Processor obligations

- Process **only on documented instructions** from the controller.
- Ensure personnel are bound by **confidentiality**.
- Implement appropriate **technical and organisational security measures** (Annex II) — see
  [security standards](../../departments/engineering/security-standards.md).
- Engage **sub-processors** only with authorisation; flow down equivalent obligations; maintain a current
  sub-processor list.
- **Assist the controller** with data-subject rights requests, DPIAs, and regulator engagement.
- **Notify the controller without undue delay** of any personal-data breach
  ([incident response](../../departments/post-launch/incident-response.md),
  [security breach playbook](../../departments/post-launch/playbooks/security-breach.md)).
- **Delete or return** all personal data at the end of the term, subject to legal retention.
- Make available information necessary to demonstrate compliance and allow **audits**.

## 3. International transfers

Identify transfer mechanism (adequacy decision, Standard Contractual Clauses, or equivalent) and any
supplementary measures. Note data residency commitments.

## 4. Annexes

- **Annex I** — details of processing (parties, categories, purposes, retention).
- **Annex II** — technical and organisational security measures.
- **Annex III** — approved sub-processors.

---

**Before signing:** counsel reviewed for each applicable jurisdiction · security measures verified with
[security](../../departments/security/README.md) · data minimised and classified
([data governance](../../../ai/agents/data/data-governance-agent.md)) · sub-processor list accurate ·
breach-notification path tested · human approval obtained.
