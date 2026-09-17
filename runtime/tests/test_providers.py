"""The provider abstraction: parsing, preflight, and JSON extraction.

No network. The HTTP providers are exercised by feeding their parsers real
response shapes, which is where vendor differences actually live.
"""

from __future__ import annotations

import os
import unittest

from companyos.config import ProviderConfig
from companyos.errors import ProviderError, ProviderUnavailableError
from companyos.providers import (
    Message,
    available_providers,
    extract_json,
    register_provider,
    resolve_provider,
)
from companyos.providers.anthropic import AnthropicProvider
from companyos.providers.openai import OpenAIProvider

from . import support


class ResolutionTest(unittest.TestCase):
    def test_every_advertised_provider_resolves(self) -> None:
        for name in available_providers():
            with self.subTest(provider=name):
                provider = resolve_provider(ProviderConfig(name=name))
                self.assertTrue(provider.model, f"{name} has no default model")

    def test_unknown_provider_is_rejected(self) -> None:
        with self.assertRaises(ProviderUnavailableError):
            resolve_provider(ProviderConfig(name="gpt9000"))

    def test_local_reuses_the_openai_protocol(self) -> None:
        provider = resolve_provider(
            ProviderConfig(name="local", base_url="http://localhost:11434/v1")
        )
        self.assertIsInstance(provider, OpenAIProvider)
        self.assertEqual(provider.base_url, "http://localhost:11434/v1")

    def test_a_custom_provider_can_be_registered(self) -> None:
        register_provider("fake", lambda config: support.provider())
        try:
            self.assertIn("fake", available_providers())
            self.assertEqual(resolve_provider(ProviderConfig(name="fake")).name, "mock")
        finally:
            from companyos.providers import _CUSTOM

            _CUSTOM.pop("fake", None)


class PreflightTest(unittest.TestCase):
    def test_mock_needs_no_credentials(self) -> None:
        self.assertIsNone(support.provider().preflight())

    def test_network_providers_demand_their_key(self) -> None:
        for cls, env in ((AnthropicProvider, "ANTHROPIC_API_KEY"), (OpenAIProvider, "OPENAI_API_KEY")):
            with self.subTest(provider=cls.__name__):
                previous = os.environ.pop(env, None)
                try:
                    with self.assertRaises(ProviderUnavailableError) as caught:
                        cls(ProviderConfig(name="x")).preflight()
                    self.assertIn(env, str(caught.exception))
                finally:
                    if previous is not None:
                        os.environ[env] = previous


class AnthropicParsingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = AnthropicProvider(ProviderConfig(name="anthropic"))

    def test_text_and_usage(self) -> None:
        completion = self.provider._parse(
            {
                "content": [{"type": "text", "text": "the answer"}],
                "usage": {"input_tokens": 11, "output_tokens": 7},
                "model": "claude-sonnet-5",
                "stop_reason": "end_turn",
            }
        )
        self.assertEqual(completion.text, "the answer")
        self.assertEqual(completion.usage.input_tokens, 11)
        self.assertEqual(completion.usage.total, 18)
        self.assertFalse(completion.wants_tools)

    def test_tool_use_blocks(self) -> None:
        completion = self.provider._parse(
            {
                "content": [
                    {"type": "text", "text": "checking"},
                    {"type": "tool_use", "id": "tu_1", "name": "read_spec",
                     "input": {"path": "ai/README.md"}},
                ],
                "usage": {},
            }
        )
        self.assertTrue(completion.wants_tools)
        self.assertEqual(completion.tool_calls[0].name, "read_spec")
        self.assertEqual(completion.tool_calls[0].arguments["path"], "ai/README.md")

    def test_tool_results_are_sent_back_in_the_vendor_shape(self) -> None:
        wire = self.provider._message(Message("tool", "file contents", tool_call_id="tu_1"))
        self.assertEqual(wire["role"], "user")
        self.assertEqual(wire["content"][0]["type"], "tool_result")
        self.assertEqual(wire["content"][0]["tool_use_id"], "tu_1")


class OpenAIParsingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = OpenAIProvider(ProviderConfig(name="openai"))

    def test_text_and_usage(self) -> None:
        completion = self.provider._parse(
            {
                "choices": [{"message": {"content": "the answer"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 11, "completion_tokens": 7},
                "model": "gpt-4o-mini",
            }
        )
        self.assertEqual(completion.text, "the answer")
        self.assertEqual(completion.usage.total, 18)
        self.assertEqual(completion.stop_reason, "stop")

    def test_tool_calls_with_json_string_arguments(self) -> None:
        completion = self.provider._parse(
            {
                "choices": [
                    {
                        "message": {
                            "content": None,
                            "tool_calls": [
                                {"id": "c1", "function": {"name": "search_specs",
                                                          "arguments": '{"query": "threat"}'}}
                            ],
                        }
                    }
                ]
            }
        )
        self.assertEqual(completion.tool_calls[0].arguments["query"], "threat")

    def test_malformed_tool_arguments_do_not_crash(self) -> None:
        completion = self.provider._parse(
            {
                "choices": [
                    {
                        "message": {
                            "tool_calls": [
                                {"id": "c1", "function": {"name": "x", "arguments": "{oops"}}
                            ]
                        }
                    }
                ]
            }
        )
        self.assertIn("_raw", completion.tool_calls[0].arguments)


class JsonExtractionTest(unittest.TestCase):
    def test_bare_json(self) -> None:
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})

    def test_fenced_json(self) -> None:
        self.assertEqual(extract_json('```json\n{"a": 1}\n```'), {"a": 1})

    def test_json_wrapped_in_prose(self) -> None:
        self.assertEqual(
            extract_json('Sure! Here is the plan:\n{"a": 1}\nHope that helps.'), {"a": 1}
        )

    def test_json_array(self) -> None:
        self.assertEqual(extract_json("[1, 2, 3]"), [1, 2, 3])

    def test_no_json_raises(self) -> None:
        with self.assertRaises(ProviderError):
            extract_json("I would rather not answer in JSON.")


class MockProviderTest(unittest.TestCase):
    def test_calls_are_recorded_for_assertions(self) -> None:
        provider = support.provider()
        support.run(
            provider.complete(
                system="sys", messages=[Message("user", "hi")], purpose="execute",
                context={"agent_id": "a", "objective": "o"},
            )
        )
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(provider.calls[0].purpose, "execute")
        self.assertIn("hi", provider.calls[0].prompt)

    def test_scripted_responses_are_returned_in_order(self) -> None:
        provider = support.provider(script={"review": ["first", "second"]})
        first = support.run(provider.complete(system="", messages=[], purpose="review"))
        second = support.run(provider.complete(system="", messages=[], purpose="review"))
        self.assertEqual(first.text, "first")
        self.assertEqual(second.text, "second")

    def test_output_is_labelled_as_simulated(self) -> None:
        provider = support.provider()
        completion = support.run(
            provider.complete(
                system="", messages=[Message("user", "x")], purpose="execute",
                context={"agent_name": "Backend Engineer Agent", "objective": "build it"},
            )
        )
        self.assertIn("simulated", completion.text.lower())

    def test_usage_is_reported(self) -> None:
        provider = support.provider()
        completion = support.run(
            provider.complete(system="a system prompt", messages=[Message("user", "hello")])
        )
        self.assertGreater(completion.usage.total, 0)


if __name__ == "__main__":
    unittest.main()
