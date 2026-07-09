#!/usr/bin/env python3
"""Verify Company OS structural conventions.

Checks that every full department has the standard 18 files + 3 subfolders, and that every agent spec
has the 11 required sections. Runs in CI (.github/workflows/docs-check.yml). Exits non-zero on any gap.
"""
import os
import re
import sys

STANDARD = [
    "README.md", "mission.md", "vision.md", "principles.md", "organization.md", "roles.md",
    "agents.md", "workflows.md", "playbooks.md", "sops.md", "decision-frameworks.md", "standards.md",
    "review-process.md", "quality-gates.md", "automation.md", "metrics.md", "dashboards.md", "tools.md",
]
SUBFOLDERS = ["templates", "checklists", "examples"]
DEPARTMENTS_ROOT = os.path.join("handbook", "departments")
AGENTS_ROOT = os.path.join("ai", "agents")
DEPARTMENT_NAMES = [
    "engineering", "product", "post-launch", "design", "research", "ai-engineering", "strategy",
    "security", "devops", "finance", "legal", "hr", "operations", "marketing", "sales",
    "customer-success", "data", "documentation", "hardware", "investor-relations",
]
FULL_DEPARTMENTS = [os.path.join(DEPARTMENTS_ROOT, name) for name in DEPARTMENT_NAMES]
SECTION_RE = re.compile(r"^##\s*\d+\.", re.M)


def main() -> int:
    problems = []

    for dept in FULL_DEPARTMENTS:
        if not os.path.isdir(dept):
            problems.append(f"department missing entirely: {dept}/")
            continue
        for f in STANDARD:
            if not os.path.exists(os.path.join(dept, f)):
                problems.append(f"{dept}/: missing {f}")
        for sub in SUBFOLDERS:
            if not os.path.isdir(os.path.join(dept, sub)):
                problems.append(f"{dept}/: missing subfolder {sub}/")

    agents = 0
    for dp, _, fns in os.walk(AGENTS_ROOT):
        for fn in fns:
            if fn.endswith(".md") and fn not in ("README.md", "agent-template.md"):
                agents += 1
                with open(os.path.join(dp, fn), encoding="utf-8") as fh:
                    n = len(SECTION_RE.findall(fh.read()))
                if n != 11:
                    problems.append(f"{os.path.join(dp, fn)}: has {n} sections, expected 11")

    print(f"Checked {len(FULL_DEPARTMENTS)} departments and {agents} agent specs.")
    if problems:
        print(f"\n{len(problems)} structural problem(s):")
        for p in problems:
            print(f"  {p}")
        return 1
    print("All departments and agent specs conform.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
