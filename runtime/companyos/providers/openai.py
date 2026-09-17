"""OpenAI-compatible Chat Completions provider.

Also serves local and third-party servers that speak the same protocol (Ollama,
vLLM, LM Studio, OpenRouter) -- point ``base_url`` at them and, for servers that
need no key, set ``api_key_env`` to an env var holding any placeholder value.
"""

from __future__ import annotations

import json
from typing import Any, Mapping

from ..config import ProviderConfig
from ..models import Usage
from . import Completion, Message, Provider, ToolCall, ToolSpec
from ._http import post_json, require_key


class OpenAIProvider(Provider):
    name = "openai"
    default_model = "gpt-4o-mini"

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self.base_url = (config.base_url or "https://api.openai.com/v1").rstrip("/")
        self.api_key_env = config.api_key_env or "OPENAI_API_KEY"

    def preflight(self) -> None:
        require_key(self.api_key_env, self.name)

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
        wire: list[dict] = []
        if system:
            wire.append({"role": "system", "content": system})
        for message in messages:
            if message.role == "tool":
                wire.append(
                    {
                        "role": "tool",
                        "tool_call_id": message.tool_call_id,
                        "content": message.content,
                    }
                )
            else:
                wire.append({"role": message.role, "content": message.content})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": wire,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": self.config.temperature if temperature is None else temperature,
        }
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": dict(t.parameters)
                        or {"type": "object", "properties": {}},
                    },
                }
                for t in tools
            ]
        payload.update(self.config.extra)

        data = await post_json(
            f"{self.base_url}/chat/completions",
            payload,
            {"authorization": f"Bearer {require_key(self.api_key_env, self.name)}"},
        )
        return self._parse(data)

    def _parse(self, data: dict) -> Completion:
        choices = data.get("choices") or [{}]
        message = choices[0].get("message", {}) or {}

        tool_calls: list[ToolCall] = []
        for call in message.get("tool_calls") or ():
            function = call.get("function", {}) or {}
            try:
                arguments = json.loads(function.get("arguments") or "{}")
            except json.JSONDecodeError:
                arguments = {"_raw": function.get("arguments", "")}
            tool_calls.append(
                ToolCall(id=call.get("id", ""), name=function.get("name", ""), arguments=arguments)
            )

        usage = data.get("usage", {}) or {}
        return Completion(
            text=(message.get("content") or "").strip(),
            tool_calls=tuple(tool_calls),
            usage=Usage(
                int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0))
            ),
            provider=self.name,
            model=data.get("model", self.model),
            stop_reason=choices[0].get("finish_reason", ""),
            raw=data,
        )
