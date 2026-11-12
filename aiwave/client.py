"""AIWave client for supported OpenAI-compatible API operations.

Usage:
    from aiwave import AIWave
    client = AIWave(api_key="YOUR_API_KEY_HERE")

    # Chat completions through the OpenAI client interface
    client.chat.completions.create(model="deepseek-v4-flash", messages=[...])

    # AI video — check the exact model and account-group access before use
    job = client.video.generate(model="kling-v2-6", prompt="A red car drifting...")
    done = client.video.wait(job.task_id)

Get your API key at: https://aiwave.live
"""
import math
import os
import time
from types import SimpleNamespace
from typing import Any, Dict
from urllib.parse import quote

from openai import OpenAI

_UNSET = object()
_MAX_POLL_INTERVAL_SECONDS = (2 ** 31 - 1) / 1000


def _valid_duration(value, minimum, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < minimum:
        return False
    if maximum is not None and value > maximum:
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


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
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        body = {"model": model, "prompt": prompt}
        body.update(kwargs)
        # OpenAI 1.x requires a parameterized mapping; 3.x accepts it too.
        # A timeout or transient error may occur after the provider accepted a
        # paid job. Retrying this POST could create another billable job.
        resp = self._client.post(
            "/video/generations",
            cast_to=Dict[str, Any],
            body=body,
            options={"max_retries": 0},
        )
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
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("status requires a non-empty task ID")
        resp = self._client.get(
            f"/video/generations/{quote(task_id, safe='')}", cast_to=Dict[str, Any]
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
            interval: seconds between polls (1 to 2147483.647; default 15)
            timeout: seconds to wait in total (default 900 = 15 minutes)
            poll: if False, returns the current status immediately

        Raises:
            TimeoutError: the job did not finish within timeout
            RuntimeError: the job failed upstream
        """
        if not poll:
            return self.status(task_id)
        if not _valid_duration(interval, 1, _MAX_POLL_INTERVAL_SECONDS):
            raise ValueError("interval must be a finite number from 1 to 2147483.647 seconds")
        if not _valid_duration(timeout, 0):
            raise ValueError("timeout must be a finite non-negative number of seconds")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            st = self.status(task_id)
            # Generic tasks use SUCCESS/FAILURE; realtime and video adapters
            # can return succeeded/failed or completed/failed.
            status = st.status.lower() if isinstance(st.status, str) else ""
            if status in {"success", "succeeded", "completed"}:
                return st
            if status in {"failure", "failed"}:
                reason = st.raw.get("fail_reason", "unknown") if isinstance(st.raw, dict) else "unknown"
                raise RuntimeError(f"Video generation failed upstream: {reason}")
            time.sleep(min(interval, max(0, deadline - time.monotonic())))
        raise TimeoutError(
            f"Video job {task_id} did not finish within {timeout}s. "
            "Keep the task ID and check its status and usage before "
            "submitting another paid job."
        )


class AIWave(OpenAI):
    """AIWave API client for compatible chat requests and video routes."""

    DEFAULT_BASE_URL = "https://aiwave.live/v1"

    def __init__(self, api_key=_UNSET, base_url=None, **kwargs):
        if api_key is _UNSET:
            api_key = os.environ.get("AIWAVE_API_KEY")
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError(
                "AIWave API key required. Pass api_key or set AIWAVE_API_KEY."
            )
        super().__init__(
            api_key=api_key,
            base_url=base_url or self.DEFAULT_BASE_URL,
            **kwargs
        )
        self.video = VideoAPI(self)
