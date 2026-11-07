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
from typing import Any, Dict

from openai import OpenAI


class VideoAPI:
    """AIWave video generation routes.

    Video routes are experimental and require an eligible paid account group.
    Completion time varies; poll `status()` and retain the task ID.
    """

    def __init__(self, client):
        self._client = client

    def generate(self, *, model="kling-v2-6", prompt, **kwargs):
        """Submit a video generation job.

        Returns a namespace with `.task_id` and `.status`.
        """
        body = {"model": model, "prompt": prompt}
        body.update(kwargs)
        # OpenAI 1.x requires a parameterized mapping; 3.x accepts it too.
        resp = self._client.post("/video/generations", cast_to=Dict[str, Any], body=body)
        data = resp.get("data", resp) if isinstance(resp, dict) else None
        task_id = data.get("task_id") or data.get("id") if isinstance(data, dict) else None
        if not isinstance(task_id, str) or not task_id:
            raise RuntimeError(
                "Video submission returned no task ID; check task history and usage "
                "before submitting another paid job."
            )
        return SimpleNamespace(
            task_id=task_id,
            status=data.get("status", "queued"),
            raw=data,
        )

    def status(self, task_id):
        """Check a video job's status.

        Returns a namespace with `.status`, `.progress` and `.raw`.
        """
        resp = self._client.get(
            f"/video/generations/{task_id}", cast_to=Dict[str, Any]
        )
        data = resp.get("data", resp) if isinstance(resp, dict) else None
        return SimpleNamespace(
            status=data.get("status", "unknown") if isinstance(data, dict) else "unknown",
            progress=data.get("progress", "") if isinstance(data, dict) else "",
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
                reason = st.raw.get("fail_reason", "unknown") if isinstance(st.raw, dict) else "unknown"
                raise RuntimeError(f"Video generation failed upstream: {reason}")
            time.sleep(interval)
        raise TimeoutError(
            f"Video job {task_id} did not finish within {timeout}s. "
            "Keep the task ID and check its status and usage before "
            "submitting another paid job."
        )


class AIWave(OpenAI):
    """AIWave API client, fully compatible with OpenAI SDK."""

    DEFAULT_BASE_URL = "https://aiwave.live/v1"

    def __init__(self, api_key=None, base_url=None, **kwargs):
        api_key = api_key or os.environ.get("AIWAVE_API_KEY")
        if not api_key:
            raise ValueError(
                "AIWave API key required. Pass api_key or set AIWAVE_API_KEY."
            )
        super().__init__(
            api_key=api_key,
            base_url=base_url or self.DEFAULT_BASE_URL,
            **kwargs
        )
        self.video = VideoAPI(self)
