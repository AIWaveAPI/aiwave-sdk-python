# AIWave Python SDK

**One OpenAI-compatible API for Chinese AI models and video. 97 model IDs on the public rate card, 10 Chinese families, 13 video IDs on the public rate card.**

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Models](https://img.shields.io/badge/model%20IDs-97-blue)](https://aiwave.live/models)
[![Video](https://img.shields.io/badge/video%20IDs-13-purple)](https://aiwave.live/models)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AIWave gives developers one OpenAI-compatible API route for Chinese AI model families — DeepSeek, GLM, Kimi, Qwen, MiniMax, Doubao, StepFun, MiMo — plus AI video routes (Kling, Seedance, Hailuo, Wan, Vidu).

The counts describe catalog-listed IDs, not access for a particular key or live
route health. Test the exact model and operation before production use.

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
The SDK does not automatically retry a video submission after a 429, 503, or
connection error: the provider may already have accepted the paid job. Check
task history and usage before deciding whether to submit again. Status polling
remains retryable.
Custom polling intervals must be 1–2,147,483.647 seconds; invalid intervals
and non-finite timeouts are rejected before a status request.

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
