"""Anthropic Messages API provider (stdlib HTTP, no SDK required)."""

from __future__ import annotations

from typing import Any, Mapping

from ..config import ProviderConfig
from ..models import Usage
from . import Completion, Message, Provider, ToolCall, ToolSpec
from ._http import post_json, require_key

_API_VERSION = "2023-06-01"


class AnthropicProvider(Provider):
    name = "anthropic"
    default_model = "claude-sonnet-5"

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self.base_url = (config.base_url or "https://api.anthropic.com").rstrip("/")
        self.api_key_env = config.api_key_env or "ANTHROPIC_API_KEY"

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
        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": self.config.temperature if temperature is None else temperature,
            "messages": [self._message(m) for m in messages],
        }
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": dict(t.parameters)
                    or {"type": "object", "properties": {}},
                }
                for t in tools
            ]
        payload.update(self.config.extra)

        data = await post_json(
            f"{self.base_url}/v1/messages",
            payload,
            {
                "x-api-key": require_key(self.api_key_env, self.name),
                "anthropic-version": _API_VERSION,
            },
        )
        return self._parse(data)

    @staticmethod
    def _message(message: Message) -> dict:
        if message.role == "tool":
            return {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": message.tool_call_id,
                        "content": message.content,
                    }
                ],
            }
        return {"role": message.role, "content": message.content}

    def _parse(self, data: dict) -> Completion:
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.get("id", ""),
                        name=block.get("name", ""),
                        arguments=block.get("input", {}) or {},
                    )
                )
        usage = data.get("usage", {})
        return Completion(
            text="\n".join(p for p in text_parts if p).strip(),
            tool_calls=tuple(tool_calls),
            usage=Usage(
                int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0))
            ),
            provider=self.name,
            model=data.get("model", self.model),
            stop_reason=data.get("stop_reason", ""),
            raw=data,
        )
