# Playbook: Handling a Customer Complaint

**When to use:** a customer is unhappy - a bug, an outage, a broken expectation, or poor service.

1. **Acknowledge fast** - respond quickly, take it seriously, and never argue. Speed of acknowledgement matters more than speed of fix.
2. **Understand the real problem** - ask what happened, what they expected, and what impact it had. Separate the incident from the underlying frustration ([support](../departments/customer-success/README.md)).
3. **Classify and route** - bug → [bug management](../departments/post-launch/bug-management.md); outage → [incident response](../departments/post-launch/incident-response.md); expectation gap → [product](../departments/product/README.md); service failure → own it.
4. **Make it right for the customer first** - restore service or provide a workaround before optimizing the fix ([customer-first recovery](../departments/post-launch/principles.md)).
5. **Communicate honestly** - what happened, what you're doing, and by when. Never over-promise a timeline ([communication rules](../governance/communication-rules.md)).
6. **Fix the root cause** - every fix ships with a reproducing test; every incident gets a blameless [postmortem](../departments/post-launch/incident-response.md).
7. **Close the loop** - tell the customer it's fixed. Check [account health](../departments/customer-success/README.md) afterward; a well-handled complaint often increases loyalty.
8. **Feed the system** - route the signal to [customer feedback](../departments/post-launch/customer-feedback.md) so patterns reach the roadmap.

**Success criteria:** customer's problem resolved, root cause fixed, relationship intact or stronger.
**Escalate if:** the account goes red → the [at-risk account playbook](../departments/customer-success/playbooks.md); the complaint indicates a systemic failure → leadership.
