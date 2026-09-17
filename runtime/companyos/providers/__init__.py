"""Provider abstraction.

The orchestrator talks to *this* interface and never to a vendor SDK. Adding a
provider means adding a module here and a line in :data:`_BUILTIN`; no
orchestration code changes.

All built-in providers use only the standard library (``urllib``), so the
runtime installs and runs with zero dependencies.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from ..config import ProviderConfig
from ..errors import ProviderError, ProviderUnavailableError
from ..models import Usage


@dataclass(frozen=True)
class Message:
    """One turn in a conversation sent to a provider."""

    role: str  # "user" | "assistant" | "tool"
    content: str
    name: str = ""
    tool_call_id: str = ""


@dataclass(frozen=True)
class ToolCall:
    """A tool invocation requested by the model."""

    id: str
    name: str
    arguments: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolSpec:
    """A tool offered to the model, in provider-neutral form."""

    name: str
    description: str
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class Completion:
    """A provider's answer, normalized across vendors."""

    text: str = ""
    tool_calls: tuple[ToolCall, ...] = ()
    usage: Usage = field(default_factory=Usage)
    provider: str = ""
    model: str = ""
    stop_reason: str = ""
    raw: Any = None

    @property
    def wants_tools(self) -> bool:
        return bool(self.tool_calls)


class Provider(ABC):
    """The contract every model backend implements."""

    name: str = "provider"

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config
        self.model = config.model or self.default_model

    #: Used when the config names no model.
    default_model: str = ""

    @abstractmethod
    async def complete(
        self,
        *,
        system: str,
        messages: list[Message],
        tools: list[ToolSpec] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        purpose: str = "",
        context: Mapping[str, Any] | None = None,
    ) -> Completion:
        """Produce one completion.

        ``purpose`` and ``context`` are routing/telemetry metadata (which
        orchestration step this call serves, which agent and task it belongs
        to). Network providers use them for tracing only; they never change the
        wire format. The mock provider uses ``purpose`` to decide what shape of
        answer to return, which is what makes offline runs exercise the real
        orchestration path.
        """

    def preflight(self) -> None:
        """Fail fast if the provider cannot possibly work.

        Called once before a run starts. Without it, a missing API key would
        surface as a per-step provider failure, and the orchestrator's graceful
        degradation would quietly turn a misconfigured run into a useless one.
        Raises :class:`ProviderUnavailableError`.
        """

    def describe(self) -> dict:
        return {"provider": self.name, "model": self.model}


# --- JSON helpers shared by every orchestration step --------------------------

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def extract_json(text: str) -> Any:
    """Pull a JSON value out of a model response.

    Models wrap JSON in prose or fences more often than not; this tries the
    whole string, then fenced blocks, then the outermost brace/bracket span.
    Raises :class:`ProviderError` when nothing parses, so callers can fall back
    deliberately instead of crashing on a stray sentence.
    """
    candidates: list[str] = [text.strip()]
    candidates += [m.group(1).strip() for m in _FENCE.finditer(text)]
    for opener, closer in (("{", "}"), ("[", "]")):
        start, end = text.find(opener), text.rfind(closer)
        if 0 <= start < end:
            candidates.append(text[start : end + 1])

    for candidate in candidates:
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ProviderError(f"no JSON found in model response: {text[:200]!r}")


def estimate_tokens(text: str) -> int:
    """Rough token count for budgeting when a provider reports no usage."""
    return max(1, len(text) // 4)


# --- registry -----------------------------------------------------------------

_BUILTIN: dict[str, str] = {
    "mock": "companyos.providers.mock:MockProvider",
    "anthropic": "companyos.providers.anthropic:AnthropicProvider",
    "openai": "companyos.providers.openai:OpenAIProvider",
    # OpenAI-compatible servers (Ollama, vLLM, LM Studio, OpenRouter) need only
    # a base_url, so they reuse the same client.
    "local": "companyos.providers.openai:OpenAIProvider",
}

_CUSTOM: dict[str, Callable[[ProviderConfig], Provider]] = {}


def register_provider(name: str, factory: Callable[[ProviderConfig], Provider]) -> None:
    """Register a provider implementation under ``name``."""
    _CUSTOM[name] = factory


def available_providers() -> list[str]:
    return sorted(set(_BUILTIN) | set(_CUSTOM))


def resolve_provider(config: ProviderConfig) -> Provider:
    """Instantiate the provider named by ``config``."""
    name = (config.name or "mock").lower()
    if name in _CUSTOM:
        return _CUSTOM[name](config)
    if name not in _BUILTIN:
        raise ProviderUnavailableError(
            f"unknown provider {name!r}; available: {', '.join(available_providers())}"
        )
    module_path, _, attr = _BUILTIN[name].partition(":")
    from importlib import import_module

    module = import_module(module_path)
    return getattr(module, attr)(config)


__all__ = [
    "Completion",
    "Message",
    "Provider",
    "ToolCall",
    "ToolSpec",
    "available_providers",
    "estimate_tokens",
    "extract_json",
    "register_provider",
    "resolve_provider",
]
