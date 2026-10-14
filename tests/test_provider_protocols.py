import importlib.util
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PROVIDER_PATH = ROOT / "基础" / "starter" / "provider.py"


def load_provider():
    spec = importlib.util.spec_from_file_location("provider_under_test", PROVIDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({
            "id": "resp_test",
            "output": [{"content": [{"type": "output_text", "text": '{"answer":"OK","citations":[]}'}]}],
            "usage": {"input_tokens": 10, "output_tokens": 2},
        }).encode("utf-8")


class ProviderProtocolTests(unittest.TestCase):
    def test_responses_endpoint_sends_input_and_max_output_tokens(self):
        provider = load_provider()
        captured = {}

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["url"] = request.full_url
            captured["timeout"] = timeout
            return FakeResponse()

        config = {
            "endpoint": "https://synapse-ai.uk/v1/responses",
            "model": "gpt-5.5",
            "parameters": {"max_output_tokens": 32},
            "timeout_seconds": 7,
        }
        with patch.dict(os.environ, {"ASSESSMENT_API_KEY": "test-key"}), patch.object(provider.urllib.request, "urlopen", fake_urlopen):
            result = provider.call_model([{"role": "user", "content": "hello"}], config)

        self.assertEqual(captured["url"], config["endpoint"])
        self.assertEqual(captured["body"]["input"][0]["content"], "hello")
        self.assertEqual(captured["body"]["max_output_tokens"], 32)
        self.assertNotIn("messages", captured["body"])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["response"]["id"], "resp_test")

    def test_chat_completions_endpoint_keeps_messages_contract(self):
        provider = load_provider()
        captured = {}

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse()

        config = {
            "endpoint": "https://example.test/v1/chat/completions",
            "model": "gpt-5.5",
            "parameters": {"max_tokens": 32},
            "timeout_seconds": 7,
        }
        with patch.dict(os.environ, {"ASSESSMENT_API_KEY": "test-key"}), patch.object(provider.urllib.request, "urlopen", fake_urlopen):
            provider.call_model([{"role": "user", "content": "hello"}], config)

        self.assertEqual(captured["body"]["messages"][0]["content"], "hello")
        self.assertFalse(captured["body"]["stream"])
        self.assertNotIn("input", captured["body"])


if __name__ == "__main__":
    unittest.main()
