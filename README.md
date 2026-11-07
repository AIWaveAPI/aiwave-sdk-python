# AIWave Python SDK

**One OpenAI-compatible API for Chinese AI models — and AI video. 97 public routes, 10 Chinese families, 13 public video routes.**

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Models](https://img.shields.io/badge/public%20rate%20card-97%20routes-blue)](https://aiwave.live/models)
[![Video](https://img.shields.io/badge/public%20video%20routes-13-purple)](https://aiwave.live/models)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AIWave gives developers one OpenAI-compatible API route for Chinese AI model families — DeepSeek, GLM, Kimi, Qwen, MiniMax, Doubao, StepFun, MiMo — plus AI video routes (Kling, Seedance, Hailuo, Wan, Vidu).

Get a key at [aiwave.live/register](https://aiwave.live/register).

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

Store API keys outside source control. The example above uses an environment variable and does not include a real key. The AIWave client accepts an explicit `api_key` or `AIWAVE_API_KEY`; it never takes `OPENAI_API_KEY` from another provider's environment.

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

## AI video

One key, video routes on Kling, Seedance, Hailuo, Wan and Vidu.

```python
from aiwave import AIWave

client = AIWave(api_key="YOUR_API_KEY_HERE")

job = client.video.generate(
    model="kling-v2-6",
    prompt="A red sports car drifting through a neon-lit city at night, cinematic tracking shot",
)
print(job.task_id)

done = client.video.wait(job.task_id)   # polls every 15s, 15 min max
print(done.status)
```

Video routes are experimental and need an eligible paid account group.
Completion time varies. Keep the task ID and check its status and usage before
submitting another paid job if polling times out.

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
