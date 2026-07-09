#!/usr/bin/env python3
"""Verify Company OS authoring conventions (see CONTRIBUTING.md and STRUCTURE.md).

Enforces the rules that keep the repository navigable and free of filler:
  1. Every content directory self-indexes with a README.md.
  2. No placeholder text - if a file isn't real, it shouldn't exist.
  3. Markdown hygiene: no tabs, no trailing whitespace, file ends with a newline.

Runs in CI (.github/workflows/docs-check.yml). Exits non-zero on any violation.
"""
import os
import re
import sys

# Directories whose Markdown is content (as opposed to tooling or GitHub metadata).
CONTENT_ROOTS = ["handbook", "ai", "starter-kits"]
# Leaf asset folders hold standalone assets indexed by their parent's README.
LEAF_ASSET_DIRS = {"checklists", "examples"}
# Directories scanned for markdown hygiene.
HYGIENE_ROOTS = CONTENT_ROOTS + [".github"]

PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|lorem ipsum|coming soon", re.IGNORECASE)


def iter_markdown(roots):
    # top-level docs (README, CUSTOMIZE, STRUCTURE, ...) are content too
    for name in sorted(os.listdir(".")):
        if name.endswith(".md") and os.path.isfile(name):
            yield name
    for base in roots:
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for name in sorted(filenames):
                if name.endswith(".md"):
                    yield os.path.join(dirpath, name)


def main() -> int:
    problems = []

    # 1. every content directory has a README.md
    dirs_checked = 0
    for base in CONTENT_ROOTS:
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            if os.path.basename(dirpath) in LEAF_ASSET_DIRS:
                continue
            if not any(f.endswith(".md") for f in filenames):
                continue
            dirs_checked += 1
            if "README.md" not in filenames:
                problems.append(f"{dirpath}: missing README.md (every folder self-indexes)")

    # 2 + 3. placeholder text and markdown hygiene
    files_checked = 0
    for path in iter_markdown(HYGIENE_ROOTS):
        files_checked += 1
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        match = PLACEHOLDER_RE.search(text)
        if match:
            line = text[: match.start()].count("\n") + 1
            problems.append(f"{path}:{line}: placeholder text {match.group(0)!r}")

        if "\t" in text:
            problems.append(f"{path}: contains a tab character")
        lines = text.split("\n")
        for n, line in enumerate(lines[:-1], 1):
            if line != line.rstrip():
                problems.append(f"{path}:{n}: trailing whitespace")
                break
        if text and not text.endswith("\n"):
            problems.append(f"{path}: does not end with a newline")

    print(f"Checked {dirs_checked} content directories and {files_checked} Markdown files.")
    if problems:
        print(f"\n{len(problems)} convention violation(s):")
        for p in problems:
            print(f"  {p}")
        return 1
    print("All conventions satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
