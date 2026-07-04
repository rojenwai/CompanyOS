# Prompt Engineering Standards

Prompts are engineered artifacts, versioned in [prompt memory](../memory/prompt-memory.md).

## Every prompt defines

- **Role** — who the agent is.
- **Objective** — what to accomplish.
- **Context** — the relevant, bounded information ([context management](../memory/context-management.md)).
- **Constraints** — rules and prohibitions.
- **Expected output** — format and structure.
- **Evaluation criteria** — how the output is judged.

## Rules

- Avoid ambiguous instructions.
- Prefer tools over guessing; never fabricate tool outputs.
- Changes are evaluated with **prompt regression tests** before becoming canonical
  ([evaluation-and-testing.md](evaluation-and-testing.md)).
- Keep context precise — overloading context degrades reasoning and raises cost.
