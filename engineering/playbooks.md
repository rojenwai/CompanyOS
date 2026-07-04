# Engineering Playbooks

Situational guides. Production-incident playbooks live in [post-launch/playbooks/](../post-launch/playbooks/);
these cover engineering-time situations.

## Playbook: failing CI on `main`
**When:** the protected branch is red.
1. Freeze merges to `main`. 2. Identify the offending commit. 3. Revert if fix is not immediate.
4. Fix forward with a test that reproduces the failure. 5. Post a note to [lessons-learned](../memory/lessons-learned.md).

## Playbook: flaky test
**When:** a test passes/fails non-deterministically.
1. Quarantine it (mark, don't delete). 2. Reproduce and find the source of nondeterminism (time, order, IO).
3. Fix root cause. 4. Un-quarantine only when stable across repeated runs.

## Playbook: large refactor
**When:** structure must change across many files.
1. Pin behavior with tests ([refactoring policy](refactoring-policy.md)). 2. Land in small, reviewable PRs.
3. Keep `main` shippable throughout. 4. Record architecture changes as [ADRs](../templates/documents/adr.md).
