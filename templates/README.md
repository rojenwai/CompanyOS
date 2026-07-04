# Templates

Reusable scaffolds used across Company OS.

| Template | Purpose |
|---|---|
| [department-template/](department-template/) | The canonical structure for a new [department](../STRUCTURE.md#standard-department-structure) — copy the whole folder. |
| [documents/](documents/) | Company-wide document templates (PRD, RFC, ADR, incident report, …). |

The agent specification template lives with the agents: [agents/agent-template.md](../agents/agent-template.md).

## How to use

- **New department?** Copy `department-template/` to `<department>/` and fill it in.
- **New document?** Copy the matching file from `documents/` into the relevant department's `templates/` or working folder.
- **New agent?** Copy `agents/agent-template.md`.

Never leave the copied placeholder text in a finished document — see [CONTRIBUTING.md](../CONTRIBUTING.md).
