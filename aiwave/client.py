"""AIWave Client — Drop-in OpenAI compatible client.

Usage:
    from aiwave import AIWave
    client = AIWave(api_key="YOUR_API_KEY_HERE")

    # Chat / reasoning — identical to the OpenAI SDK
    client.chat.completions.create(model="deepseek-v4-flash", messages=[...])

    # AI video — one key, 13 video routes
    job = client.video.generate(model="kling-v2-6", prompt="A red car drifting...")
    done = client.video.wait(job.task_id)

Get your API key at: https://aiwave.live
"""
import os
import time
from types import SimpleNamespace

from openai import OpenAI


class VideoAPI:
    """AIWave video generation routes.

    Video routes are experimental and require a paid account group (from $5).
    A single shot takes 5-11 minutes; poll `status()` until it reports success.
    """

    def __init__(self, client):
        self._client = client

    def generate(self, *, model="kling-v2-6", prompt, **kwargs):
        """Submit a video generation job.

        Returns a namespace with `.task_id` and `.status`.
        """
        body = {"model": model, "prompt": prompt}
        body.update(kwargs)
        resp = self._client.post("/video/generations", cast_to=SimpleNamespace, body=body)
        data = getattr(resp, "data", resp)
        task_id = getattr(data, "task_id", None) or getattr(data, "id", None)
        return SimpleNamespace(
            task_id=task_id,
            status=getattr(data, "status", "queued"),
            raw=data,
        )

    def status(self, task_id):
        """Check a video job's status.

        Returns a namespace with `.status`, `.progress` and `.raw`.
        """
        resp = self._client.get(
            f"/video/generations/{task_id}", cast_to=SimpleNamespace
        )
        data = getattr(resp, "data", resp)
        return SimpleNamespace(
            status=getattr(data, "status", "unknown"),
            progress=getattr(data, "progress", ""),
            raw=data,
        )

    def wait(self, task_id, *, interval=15, timeout=900, poll=True):
        """Poll a job until it succeeds, fails, or times out.

        Args:
            task_id: the id returned by generate()
            interval: seconds between polls (default 15)
            timeout: seconds to wait in total (default 900 = 15 minutes)
            poll: if False, returns the current status immediately

        Raises:
            TimeoutError: the job did not finish within timeout
            RuntimeError: the job failed upstream
        """
        if not poll:
            return self.status(task_id)
        deadline = time.time() + timeout
        while time.time() < deadline:
            st = self.status(task_id)
            if st.status == "SUCCESS":
                return st
            if st.status == "FAILURE":
                reason = getattr(st.raw, "fail_reason", "unknown")
                raise RuntimeError(f"Video generation failed upstream: {reason}")
            time.sleep(interval)
        raise TimeoutError(
            f"Video job {task_id} did not finish within {timeout}s. "
            "Single shots take 5-11 minutes; if it stays at 0% progress for "
            "over 3 minutes, the upstream channel likely failed — submit again."
        )


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
        self.video = VideoAPI(self)
