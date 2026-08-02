# AIWave Python SDK

One API key for 48 Chinese AI models — OpenAI compatible, with a drop-in OpenAI SDK interface.

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Live model catalog

The catalog and USD token prices change over time. See the [live AIWave pricing page](https://aiwave.live/pricing) for the current 48-model catalog instead of relying on a hard-coded list.

## Installation

```bash
pip install aiwave
```

## Quick Start

```python
from aiwave import AIWave

client = AIWave(api_key="YOUR_API_KEY_HERE")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Explain quantum computing in 3 sentences"}]
)
print(response.choices[0].message.content)
```

Replace `YOUR_API_KEY_HERE` with a key from [aiwave.live](https://aiwave.live). Never commit a real API key to a repository.

## Drop-in OpenAI Replacement

Already using the OpenAI SDK? Change only the base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY_HERE",
    base_url="https://aiwave.live/v1"
)
# Everything else stays the same
```

## Why AIWave?

- **One API key** for 48 Chinese AI models
- **OpenAI compatible** — keep your existing SDK and tools
- **Pay-as-you-go** USD billing with no minimum deposit
- **$1 free credit** on signup for testing

## Resources

- [Live pricing and model catalog](https://aiwave.live/pricing)
- [AIWave developer blog](https://aiwave.live/blog/)
- [Node.js SDK](https://github.com/AIWaveAPI/aiwave-sdk-node)
- [Get an API key](https://aiwave.live)

## License

MIT — [AIWave](https://aiwave.live)