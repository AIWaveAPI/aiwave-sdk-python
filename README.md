# AIWave Python SDK

**One API key for 50+ Chinese AI models — OpenAI compatible, zero code changes.**

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Supported Models

- **DeepSeek**: V4 Pro, V3, R1 (Reasoning)
- **GLM**: GLM-5.1, GLM-5, GLM-4-Flash
- **Kimi**: Kimi VL (Vision), Kimi Thinking
- **ERNIE**: ERNIE 4.5, ERNIE Speed
- **Qwen**: Qwen 3, Qwen 3 VL
- *50+ more models*

## Installation

```bash
pip install aiwave
```

## Quick Start

```python
from aiwave import AIWave

client = AIWave(api_key="sk-your-key-here")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Explain quantum computing in 3 sentences"}]
)
print(response.choices[0].message.content)
```

## Drop-in OpenAI Replacement

Already using the OpenAI SDK? Just swap the base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key-here",
    base_url="https://aiwave.live/v1"
)
# Everything else stays the same
```

## Why AIWave?

- **One API key** for 50+ models — no per-model registration
- **Pay-as-you-go** — only pay what you use, no minimum deposit
- **Start free** — free credits on signup
- **OpenAI compatible** — works with your existing code and tools

**[Get your API key →](https://aiwave.live)**

## License

MIT — [AIWave](https://aiwave.live)
