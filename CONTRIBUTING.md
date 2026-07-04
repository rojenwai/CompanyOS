# Contributing to Company OS

Company OS is built **incrementally** and to **production quality**. This guide explains how to add
or extend content so the system stays consistent.

---

## Golden rules

1. **Never write placeholder text.** If you cannot write a section for real, leave it out and note it under *Future Improvements*.
2. **Follow the conventions in [STRUCTURE.md](STRUCTURE.md).** Departments, agents, and documents all have a fixed shape.
3. **Prefer depth over breadth.** Finish one thing completely before starting the next.
4. **Keep terminology consistent** with [GLOSSARY.md](GLOSSARY.md).
5. **Cross-link** every new file to the parts of the system it touches, using relative paths.

---

## Adding a new department

1. Copy [`templates/department-template/`](templates/department-template/) to `<department>/`.
2. Fill in every file. Start with `README.md`, `mission.md`, `principles.md`, then the operational files.
3. Create the department's agents under `agents/<department>/` from [`agents/agent-template.md`](agents/agent-template.md), and index them in `<department>/agents.md`.
4. Add the department to the repository map in the root [README.md](README.md) and to [STRUCTURE.md](STRUCTURE.md).

## Adding a new agent

1. Copy [`agents/agent-template.md`](agents/agent-template.md) to `agents/<division>/<agent-name>.md`.
2. Complete all **11 sections** — an agent spec is incomplete if any section is missing.
3. Register it in [`agents/README.md`](agents/README.md) and the owning department's `agents.md`.

## Adding a starter kit

1. Create `starter-kits/<company-type>/`.
2. Write a `README.md` that explains what it **inherits** from core Company OS and what it **overrides or adds**.
3. Only include the domain-specific deltas — do not duplicate core content; link to it.

---

## Style

- **Markdown** throughout. Use tables for structured comparisons, fenced code blocks for diagrams/trees.
- **Headings** are sentence-descriptive and unique within a file.
- **Lists over prose** for procedures, checklists, and criteria.
- **Relative links** only (`../orchestration/README.md`), never absolute paths or external mirrors of internal content.

---

## Review before merge

Every change should satisfy:

- [ ] Follows the standard structure for its type (department / agent / document).
- [ ] No placeholder or filler text.
- [ ] All internal links resolve.
- [ ] Terminology matches the glossary.
- [ ] Cross-links to related areas are present.
- [ ] The root README map and STRUCTURE.md are updated if a new top-level area was added.
