# AIWave Python SDK

**One OpenAI-compatible API for Chinese AI models — and AI video. 128 live routes, 9 families, 13 video generation routes.**

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Models](https://img.shields.io/badge/models-128%20live%20routes-blue)](https://aiwave.live/models)
[![Video](https://img.shields.io/badge/video-13%20generation%20routes-purple)](https://aiwave.live/models)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AIWave gives developers one OpenAI-compatible API route for Chinese AI model families — DeepSeek, GLM, Kimi, Qwen, ERNIE, MiniMax, Doubao, StepFun, MiMo — plus AI video routes (Kling, Seedance, Hailuo, Wan, Vidu).

Get a key at [aiwave.live/register](https://aiwave.live/register) — free tier included.

Use this SDK when you want a Python client path to AIWave while keeping model IDs, dated USD rates, and request-level usage evidence visible during testing.

## Installation

```bash
pip install aiwave
```

## Quick start with the AIWave client

```python
import os
from aiwave import AIWave

client = AIWave(api_key=os.environ["AIWAVE_API_KEY"])

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.choices[0].message.content)
print(response.usage)
```

Store API keys outside source control. The example above uses an environment variable and does not include a real key.

## OpenAI-compatible client path

For supported chat requests, you can also use the official OpenAI Python client with the AIWave base URL:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AIWAVE_API_KEY"],
    base_url="https://aiwave.live/v1",
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.usage)
```

## What to verify before production

- Confirm the current model ID in the [AIWave model catalog](https://aiwave.live/models/).
- Check the dated USD rates on the [AIWave pricing page](https://aiwave.live/pricing).
- Run one representative workload and review the request-level usage record.
- Keep timeout, retry, privacy, and model-quality acceptance checks in your own application.

## Resources

- [AIWave home](https://aiwave.live/)
- [Live pricing and model catalog](https://aiwave.live/pricing)
- [API docs](https://aiwave.live/docs/)
- [Developer field notes](https://aiwave.live/blog/)
- [Node.js SDK](https://github.com/AIWaveAPI/aiwave-sdk-node)

## License

MIT — [AIWave](https://aiwave.live)
