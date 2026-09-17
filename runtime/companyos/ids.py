"""Identifier and clock helpers.

Everything that makes a run non-deterministic is funnelled through here so
tests can pin it. ``freeze()`` installs a deterministic id sequence and clock.
"""

from __future__ import annotations

import itertools
import time
import uuid
from contextlib import contextmanager
from typing import Callable, Iterator

_counter = itertools.count(1)
_deterministic = False
_clock: Callable[[], float] = time.time


def new_id(prefix: str) -> str:
    """Return a short, prefixed, unique id such as ``task_3f9a1c``."""
    if _deterministic:
        return f"{prefix}_{next(_counter):06d}"
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def now() -> float:
    """Current wall-clock time, as a float epoch."""
    return _clock()


def iso(ts: float | None = None) -> str:
    """Format a timestamp as an ISO-8601 UTC string."""
    from datetime import datetime, timezone

    return datetime.fromtimestamp(now() if ts is None else ts, timezone.utc).isoformat()


@contextmanager
def freeze(start: float = 1_700_000_000.0, step: float = 1.0) -> Iterator[None]:
    """Make ids sequential and the clock advance by ``step`` per read.

    Used by tests so run snapshots and Agent Map exports compare byte-for-byte.
    """
    global _deterministic, _clock, _counter
    prev_det, prev_clock, prev_counter = _deterministic, _clock, _counter
    ticks = itertools.count()
    _deterministic = True
    _counter = itertools.count(1)
    _clock = lambda: start + step * next(ticks)  # noqa: E731
    try:
        yield
    finally:
        _deterministic, _clock, _counter = prev_det, prev_clock, prev_counter
