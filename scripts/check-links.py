#!/usr/bin/env python3
"""Verify that every relative Markdown link in the repository resolves to a real file.

Run locally with `python scripts/check-links.py`; also runs in CI
(.github/workflows/docs-check.yml). Exits non-zero if any internal link is broken.
"""
import os
import re
import sys

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:")


def main() -> int:
    root = os.getcwd()
    broken = []
    files = 0
    links = 0
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath.split(os.sep):
            continue
        for name in filenames:
            if not name.endswith(".md"):
                continue
            files += 1
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for match in LINK_RE.finditer(text):
                target = match.group(1).strip()
                if target.startswith(SKIP_PREFIXES):
                    continue
                rel = target.split("#", 1)[0]
                if not rel:
                    continue
                links += 1
                resolved = os.path.normpath(os.path.join(dirpath, rel))
                if not os.path.exists(resolved):
                    broken.append((os.path.relpath(path, root), target))

    print(f"Scanned {files} Markdown files and {links} internal links.")
    if broken:
        print(f"\n{len(broken)} broken link(s):")
        for src, target in broken:
            print(f"  {src} -> {target}")
        return 1
    print("All internal links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
