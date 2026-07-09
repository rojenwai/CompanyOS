# Customize Company OS

Company OS ships as a complete, working system. Making it *yours* is mostly **deleting what you don't
need** and **filling in who you are**. This page tells you exactly what to touch, in what order.

## The two sides

```
handbook/   ← what humans READ           ai/   ← what the AI WORKFORCE runs on
   your company's operating manual          agent specs, orchestration, memory
```

Change the **handbook** to describe how *your* company works.
Change **ai/** to change which agents exist and how work is routed.
Everything else (`scripts/`, `.github/`, `STRUCTURE.md`) is framework plumbing — leave it alone.

---

## Customize in this order

### 1. Make it your company (30 minutes)
Edit these five files. They are the only place your identity is defined; everything else refers back to them.

| File | What to write |
|---|---|
| [handbook/company/mission.md](handbook/company/mission.md) | Why your company exists |
| [handbook/company/vision.md](handbook/company/vision.md) | Where it's going (3 horizons) |
| [handbook/company/principles.md](handbook/company/principles.md) | Your non-negotiables |
| [handbook/company/structure.md](handbook/company/structure.md) | Your org shape |
| [handbook/company/roles.md](handbook/company/roles.md) | Who owns what |

### 2. Pick a starter kit (10 minutes)
Choose the [starter kit](starter-kits/README.md) matching your company type — `ai-startup`, `saas`,
`enterprise-b2b`, `marketplace`, `robotics`, `iot`, `research-lab`, and more. It tells you which
departments to activate first and adds domain-specific standards and workflows. **Delete the other kits.**

### 3. Keep only the departments you need (30 minutes)
You almost certainly do not need all twenty on day one. A typical early-stage software company runs
`product`, `engineering`, `design`, `post-launch`, and `strategy`.

**To remove a department:**
1. Delete `handbook/departments/<name>/`
2. Delete `ai/agents/<name>/`
3. Remove its rows from [handbook/departments/README.md](handbook/departments/README.md), the root [README.md](README.md), and [ai/agents/README.md](ai/agents/README.md)
4. Remove it from `DEPARTMENT_NAMES` in [scripts/check-structure.py](scripts/check-structure.py)
5. Run `python scripts/check-links.py` and fix any links that pointed into it

**To add one:**

```bash
python scripts/scaffold.py department <name>
```

This copies [the department template](handbook/templates/department-template/) into
`handbook/departments/<name>/`, creates `ai/agents/<name>/`, and prints the indexes you still need to
update. Then fill in every file — never leave placeholder text.

### 4. Choose your agents (20 minutes)
Open [ai/agents/README.md](ai/agents/README.md). Keep the agents you'll actually run; delete the rest.
To add one:

```bash
python scripts/scaffold.py agent <department> <agent-name>
```

Then fill in all 11 sections of the [standard spec](ai/agents/agent-template.md).

### 5. Tune the rules (ongoing)
Adjust [governance/quality-gates.md](handbook/governance/quality-gates.md), the
[decision framework](handbook/governance/decision-framework.md), and the department `standards.md` files to
match how strict you want to be. Tighten as you grow.

---

## What to edit, at a glance

| | Files | Guidance |
|---|---|---|
| ✏️ **Always** | `handbook/company/*`, `ai/agents/*` | This *is* your company and your workforce |
| ⚙️ **Often** | department `standards.md`, `metrics.md`, `quality-gates.md`, `governance/*` | Tune to your bar |
| 📖 **Read, don't edit** | `handbook/guides/*` | Guidance for you, not config |
| 🔒 **Leave alone** | `handbook/templates/*`, `STRUCTURE.md`, `scripts/*`, `.github/*` | The framework that keeps it consistent |

---

## Verify your changes

Three checks keep the repo healthy — all run in CI on every push and PR:

```bash
python scripts/check-links.py        # every internal link resolves
python scripts/check-structure.py    # departments + agent specs conform
python scripts/check-conventions.py  # every folder self-indexes; no placeholder text
```

Run them after any delete or rename. If you removed a department, `check-links.py` will point you at
every link that still references it.

---

## Conventions worth keeping

These are what make the system predictable — and cheap to extend:

- **Every folder has a `README.md`** that indexes it.
- **Every department has the same 18 files** ([standard structure](STRUCTURE.md#standard-department-structure)).
- **Every agent has the same 11 sections** ([standard spec](ai/agents/agent-template.md)).
- **No placeholder text.** If a file isn't real, delete it rather than leaving a stub.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full authoring conventions.
