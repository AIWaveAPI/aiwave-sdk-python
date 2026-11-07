"""A different provider's environment key must never become an AIWave key."""

import os
import importlib
from importlib.metadata import version
import unittest
from unittest.mock import patch

from aiwave import AIWave

httpx = importlib.import_module("httpx2" if int(version("openai").split(".")[0]) >= 3 else "httpx")


class KeyIsolationTests(unittest.TestCase):
    def make_client(self, **kwargs):
        transport = httpx.Client(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={})))
        client = AIWave(http_client=transport, **kwargs)
        self.addCleanup(client.close)
        return client

    def test_openai_key_alone_is_rejected(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic-other-provider"}, clear=True):
            with self.assertRaisesRegex(ValueError, "AIWave API key"):
                AIWave()

    def test_aiwave_env_key_is_used(self):
        with patch.dict(os.environ, {"AIWAVE_API_KEY": "synthetic-aiwave",
                                  "OPENAI_API_KEY": "synthetic-other-provider"}, clear=True):
            client = self.make_client()
            self.assertEqual(client.api_key, "synthetic-aiwave")

    def test_explicit_key_wins(self):
        with patch.dict(os.environ, {"AIWAVE_API_KEY": "synthetic-env"}, clear=True):
            client = self.make_client(api_key="synthetic-explicit")
            self.assertEqual(client.api_key, "synthetic-explicit")


if __name__ == "__main__":
    unittest.main()
