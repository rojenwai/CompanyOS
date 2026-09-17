"""Minimal JSON-over-HTTPS client shared by the network providers.

Uses ``urllib`` so the runtime has no third-party dependencies. Calls run in a
worker thread, so an ``await`` on one provider never blocks the scheduler from
starting the other parallel agents.
"""

from __future__ import annotations

import asyncio
import json
import os
import urllib.error
import urllib.request
from typing import Any, Mapping

from ..errors import ProviderError, ProviderUnavailableError

_RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504}


def require_key(env_var: str, provider: str) -> str:
    key = os.environ.get(env_var, "").strip()
    if not key:
        raise ProviderUnavailableError(
            f"{provider} provider needs {env_var} in the environment. "
            f"Use --provider mock to run without a model."
        )
    return key


async def post_json(
    url: str,
    payload: Mapping[str, Any],
    headers: Mapping[str, str],
    *,
    timeout: float = 120.0,
    retries: int = 2,
) -> dict:
    """POST JSON and return the decoded response, retrying transient failures."""
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return await asyncio.to_thread(_post_sync, url, payload, headers, timeout)
        except ProviderError as exc:
            last = exc
            if not getattr(exc, "retryable", False) or attempt == retries:
                raise
            await asyncio.sleep(min(2.0 * (2**attempt), 8.0))
    raise last or ProviderError("request failed")  # pragma: no cover - unreachable


def _post_sync(url: str, payload: Mapping[str, Any], headers: Mapping[str, str], timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("content-type", "application/json")
    for key, value in headers.items():
        request.add_header(key, value)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        error = ProviderError(f"HTTP {exc.code} from {url}: {detail}")
        error.retryable = exc.code in _RETRYABLE_STATUS  # type: ignore[attr-defined]
        raise error from exc
    except urllib.error.URLError as exc:
        error = ProviderError(f"cannot reach {url}: {exc.reason}")
        error.retryable = True  # type: ignore[attr-defined]
        raise error from exc
    except json.JSONDecodeError as exc:
        raise ProviderError(f"non-JSON response from {url}: {exc}") from exc
