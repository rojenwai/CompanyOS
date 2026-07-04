# Playbook: Emergency Hotfix

**When to use:** an urgent production fix is needed that [rollback](rollback.md) cannot resolve. Governed
by the [hotfix policy](../hotfix-policy.md).

1. **Scope minimally** — fix only the failing behavior.
2. **Branch** `hotfix/<name>` off the release branch ([engineering workflow](../../engineering/workflows.md)).
3. **Add a test** reproducing the issue.
4. **Expedited review** — [Reviewer](../../orchestration/reviewer.md) + [Security Reviewer](../../orchestration/security-reviewer.md) if relevant; gates compressed, not skipped.
5. **Approve & deploy** — production change requires [approval](../../orchestration/approval-engine.md); deploy phased; verify.
6. **Back-merge** into `develop`/`main` so the fix survives the next release.

**Success criteria:** issue resolved with minimal, reviewed, tested change; fix back-merged.
**Escalate if:** the fix is not obviously safe → prefer [rollback](rollback.md) and fix forward calmly.
