#!/usr/bin/env python3
"""Run the runtime test suite with no dependencies.

    python runtime/run_tests.py [-v] [pattern]

Equivalent to ``python -m unittest discover`` from the ``runtime/`` directory,
but runnable from anywhere in the repository. Also runs under pytest if you
have it (``pytest runtime/tests``); neither is required by the other.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(HERE))
    pattern = next((a for a in argv if not a.startswith("-")), "test_*.py")
    verbosity = 2 if "-v" in argv else 1

    suite = unittest.defaultTestLoader.discover(
        start_dir=str(HERE / "tests"), pattern=pattern, top_level_dir=str(HERE)
    )
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
