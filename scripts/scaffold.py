#!/usr/bin/env python3
"""Scaffold a new department or agent from the Company OS templates.

Usage:
    python scripts/scaffold.py department <name>
    python scripts/scaffold.py agent <department> <agent-name>

Examples:
    python scripts/scaffold.py department partnerships
    python scripts/scaffold.py agent engineering performance-engineer

Both commands refuse to overwrite anything that already exists. After scaffolding, fill in every file
(never leave placeholder text), add the new area to the relevant indexes, and run the checks:

    python scripts/check-links.py
    python scripts/check-structure.py
    python scripts/check-conventions.py
"""
import os
import re
import shutil
import sys

DEPT_TEMPLATE = os.path.join("handbook", "templates", "department-template")
DEPT_ROOT = os.path.join("handbook", "departments")
AGENT_TEMPLATE = os.path.join("ai", "agents", "agent-template.md")
AGENTS_ROOT = os.path.join("ai", "agents")

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def die(msg: str) -> "int":
    print(f"error: {msg}", file=sys.stderr)
    return 1


def titleize(slug: str) -> str:
    return slug.replace("-", " ").title()


def scaffold_department(name: str) -> int:
    if not SLUG_RE.match(name):
        return die(f"department name must be lowercase-hyphenated, got {name!r}")
    if not os.path.isdir(DEPT_TEMPLATE):
        return die(f"missing template at {DEPT_TEMPLATE}")
    dest = os.path.join(DEPT_ROOT, name)
    if os.path.exists(dest):
        return die(f"{dest} already exists")

    shutil.copytree(DEPT_TEMPLATE, dest)
    title = titleize(name)
    for dirpath, _, filenames in os.walk(dest):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            text = text.replace("<Department>", title).replace("<department>", name)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)

    agents_dir = os.path.join(AGENTS_ROOT, name)
    os.makedirs(agents_dir, exist_ok=True)

    print(f"Created {dest}/ and {agents_dir}/\n")
    print("Next steps:")
    print(f"  1. Fill in every file in {dest}/ - no placeholder text.")
    print(f"  2. Add agents:  python scripts/scaffold.py agent {name} <agent-name>")
    print(f"  3. Index it in handbook/departments/README.md and the root README.md.")
    print(f"  4. Add {name!r} to DEPARTMENT_NAMES in scripts/check-structure.py.")
    print("  5. Run the three checks (see this script's docstring).")
    return 0


def scaffold_agent(department: str, agent: str) -> int:
    if not SLUG_RE.match(department) or not SLUG_RE.match(agent):
        return die("department and agent names must be lowercase-hyphenated")
    if not os.path.isfile(AGENT_TEMPLATE):
        return die(f"missing template at {AGENT_TEMPLATE}")
    dept_dir = os.path.join(DEPT_ROOT, department)
    if not os.path.isdir(dept_dir):
        return die(f"no such department: {dept_dir} (create it first)")

    dest_dir = os.path.join(AGENTS_ROOT, department)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"{agent}.md")
    if os.path.exists(dest):
        return die(f"{dest} already exists")

    with open(AGENT_TEMPLATE, encoding="utf-8") as fh:
        text = fh.read()
    title = titleize(agent)
    text = text.replace("<Agent Name>", title).replace("<agent-name>", agent)
    text = text.replace("<Department>", titleize(department)).replace("<department>", department)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    print(f"Created {dest}\n")
    print("Next steps:")
    print("  1. Fill in all 11 sections - no placeholder text.")
    print(f"  2. Index it in {dest_dir}/README.md and {dept_dir}/agents.md.")
    print("  3. Run the three checks (see this script's docstring).")
    return 0


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "department" and len(argv) == 3:
        return scaffold_department(argv[2])
    if cmd == "agent" and len(argv) == 4:
        return scaffold_agent(argv[2], argv[3])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
