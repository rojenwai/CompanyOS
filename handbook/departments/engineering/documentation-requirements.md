# Documentation Requirements

Every project includes: README · Architecture · Installation · Configuration · Deployment ·
Troubleshooting · Contribution Guide · API Reference.

## Code documentation

Every public function documents its **purpose, inputs, outputs, errors, and an example**. Complex
algorithms explain **why**, not **what**.

## Rules

- Docs ship with the change, not after — the [Documentation Reviewer](../../../ai/orchestration/documentation-reviewer.md) gates release.
- One canonical version per document (tracked in [documentation memory](../../../ai/memory/documentation-memory.md)).
- Drift is detected and repaired by the [Documentation Maintenance Agent](../../../ai/agents/post-launch/documentation-maintenance-agent.md).

Reusable document templates live in [templates/documents/](../../templates/documents/).
