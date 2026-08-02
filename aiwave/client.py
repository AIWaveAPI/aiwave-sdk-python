"""AIWave Client — Drop-in OpenAI compatible client.

Usage:
    from aiwave import AIWave
    client = AIWave(api_key="YOUR_API_KEY_HERE")

Get your API key at: https://aiwave.live
"""
import os
from openai import OpenAI


class AIWave(OpenAI):
    """AIWave API client, fully compatible with OpenAI SDK."""

    DEFAULT_BASE_URL = "https://aiwave.live/v1"

    def __init__(self, api_key=None, base_url=None, **kwargs):
        api_key = api_key or os.environ.get("AIWAVE_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key required. Get one at https://aiwave.live or set AIWAVE_API_KEY env var."
            )
        super().__init__(
            api_key=api_key,
            base_url=base_url or self.DEFAULT_BASE_URL,
            **kwargs
        )
