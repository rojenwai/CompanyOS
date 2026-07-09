# Engineering SOPs

Routine procedures. Each is short, numbered, and unambiguous.

## SOP-01: Start a feature
1. Confirm the task meets the [Definition of Ready](definition-of-ready.md).
2. Branch `feature/<name>` from `develop`.
3. Implement in small commits ([Conventional Commits](workflows.md)).
4. Add tests for every acceptance criterion.
5. Open a PR with the required sections.

## SOP-02: Merge a change
1. Ensure CI is green and coverage targets met.
2. Obtain the required reviews (2, or 3 for critical infra).
3. Confirm [security](security-standards.md) and [docs](documentation-requirements.md) sign-off if applicable.
4. Squash-merge with a clean message; delete the branch.

## SOP-03: Add a dependency
1. Answer the [dependency rules](standards.md#dependency-rules) questions.
2. Check license compatibility with [legal](../../company/roles.md).
3. Run a dependency/security scan.
4. Record the rationale in the PR.

## SOP-04: Ship a release
Follow the [release checklist](../../templates/documents/release-checklist.md) and the
[SDLC deployment phase](../../workflows/sdlc.md).
