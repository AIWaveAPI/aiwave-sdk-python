# AIWave Python SDK

**OpenAI-compatible chat for catalog-listed model IDs, with video on a separate API path.**

[![PyPI](https://img.shields.io/pypi/v/aiwave)](https://pypi.org/project/aiwave/)
[![Models](https://img.shields.io/badge/model%20IDs-91-blue)](https://aiwave.live/models)
[![Video](https://img.shields.io/badge/video%20IDs-13-purple)](https://aiwave.live/models)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The live card lists 91 model IDs on the public rate card across 10 Chinese
model families and international providers. Of those 91 IDs, 13 video IDs on
the public rate card are for video generation, so the video count is a subset
and not an additional 13. Chat requests use the OpenAI-compatible path below;
video jobs use separate `/video/generations` methods and are not Chat
Completions requests.

These counts describe catalog-listed IDs only. They are not access for a
particular key and not live route health; test the exact model and operation
before production use.

Get a key at [aiwave.live/register](https://aiwave.live/register).

Set `AIWAVE_API_KEY` through the secure shell setup in the
[Quickstart](https://github.com/AIWaveAPI/aiwave-quickstart#1-set-your-environment),
then run the examples below. The client raises if neither an explicit `api_key`
nor `AIWAVE_API_KEY` is set.

Use this client for the supported chat methods below. It also exposes the
experimental video job methods shown later in this README.

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

Video routes on Kling, Seedance, Hailuo, Wan and Vidu use the same key but a
separate API path from chat. Video IDs are a subset of the 91 catalog IDs; not
every video ID bills the same way. `kling-v2-6` is per-call, while some
Seedance IDs are token-priced. Check `quota_type` in the live card before
estimating spend.

```python
import os
from aiwave import AIWave

client = AIWave(api_key=os.environ["AIWAVE_API_KEY"])

job = client.video.generate(
    model="kling-v2-6",
    prompt="A red sports car drifting through a neon-lit city at night, cinematic tracking shot",
)
print(job.task_id)

done = client.video.wait(job.task_id)   # polls every 15s; 15 min deadline
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
`wait(timeout=...)` checks its deadline before and after each status request.
An in-flight synchronous request can still outlast that deadline. Set an
appropriate per-request `timeout` on `AIWave(...)` when your application needs
a tighter wall-clock bound; custom HTTP transports may ignore request timeouts.

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
