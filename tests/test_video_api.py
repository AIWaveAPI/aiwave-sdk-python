"""Exercise video calls through the installed OpenAI transport without network access."""

import importlib
from importlib.metadata import version
import unittest

from aiwave import AIWave


transport_module = "httpx2" if int(version("openai").split(".")[0]) >= 3 else "httpx"
httpx = importlib.import_module(transport_module)


class VideoAPITests(unittest.TestCase):
    def client_with_responses(self, submit, poll=None):
        seen = []

        def handler(request):
            seen.append((request.method, request.url.path))
            body = submit if request.method == "POST" else poll
            return httpx.Response(200, json=body)

        client = AIWave(
            api_key="synthetic-only",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
            max_retries=0,
        )
        self.addCleanup(client.close)
        return client, seen

    def test_submission_and_status_parse_nested_json(self):
        client, seen = self.client_with_responses(
            {"data": {"task_id": "synthetic-task", "status": "IN_PROGRESS"}},
            {"data": {"status": "SUCCESS", "progress": "100%"}},
        )
        job = client.video.generate(model="synthetic-model", prompt="synthetic prompt")
        state = client.video.status(job.task_id)
        self.assertEqual((job.task_id, job.status), ("synthetic-task", "IN_PROGRESS"))
        self.assertEqual((state.status, state.progress), ("SUCCESS", "100%"))
        self.assertEqual(seen, [("POST", "/v1/video/generations"),
                                ("GET", "/v1/video/generations/synthetic-task")])

    def test_status_treats_opaque_task_id_as_one_path_segment(self):
        seen = []

        def handler(request):
            seen.append(str(request.url))
            return httpx.Response(200, json={"data": {"status": "SUCCESS"}})

        client = AIWave(
            api_key="synthetic-only",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
            max_retries=0,
        )
        self.addCleanup(client.close)
        client.video.status("job/part?mode=unsafe#fragment")
        self.assertEqual(
            seen, ["https://aiwave.live/v1/video/generations/job%2Fpart%3Fmode%3Dunsafe%23fragment"]
        )

    def test_status_refuses_empty_task_id_before_network(self):
        seen = []

        def handler(request):
            seen.append(str(request.url))
            raise AssertionError("request should not be sent")

        client = AIWave(
            api_key="synthetic-only",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )
        self.addCleanup(client.close)
        with self.assertRaisesRegex(ValueError, "non-empty task ID"):
            client.video.status("")
        self.assertEqual(seen, [])

    def test_missing_task_id_does_not_look_like_success(self):
        client, _ = self.client_with_responses({"data": {"status": "IN_PROGRESS"}})
        with self.assertRaisesRegex(RuntimeError, "task ID") as caught:
            client.video.generate(model="synthetic-model", prompt="synthetic prompt")
        self.assertIn("check task history and usage", str(caught.exception))

    def test_failed_status_exposes_reason_without_resubmitting(self):
        client, _ = self.client_with_responses(
            {"data": {"task_id": "synthetic-task"}},
            {"data": {"status": "FAILURE", "fail_reason": "synthetic upstream error"}},
        )
        with self.assertRaisesRegex(RuntimeError, "synthetic upstream error"):
            client.video.wait("synthetic-task", interval=0, timeout=1)

    def test_transient_submission_failure_is_not_resubmitted(self):
        for status in (429, 503):
            with self.subTest(status=status):
                seen = []

                def handler(request):
                    seen.append(request.method)
                    if len(seen) == 1:
                        return httpx.Response(status, json={"error": {"message": "busy"}})
                    return httpx.Response(200, json={"data": {"task_id": "duplicate"}})

                client = AIWave(
                    api_key="synthetic-only",
                    http_client=httpx.Client(transport=httpx.MockTransport(handler)),
                )
                try:
                    with self.assertRaises(Exception):
                        client.video.generate(model="synthetic-model", prompt="synthetic prompt")
                    self.assertEqual(seen, ["POST"])
                finally:
                    client.close()

    def test_connection_failure_is_not_resubmitted(self):
        seen = []

        def handler(request):
            seen.append(request.method)
            raise httpx.ConnectError("synthetic disconnect")

        client = AIWave(
            api_key="synthetic-only",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )
        try:
            with self.assertRaises(Exception):
                client.video.generate(model="synthetic-model", prompt="synthetic prompt")
            self.assertEqual(seen, ["POST"])
        finally:
            client.close()


if __name__ == "__main__":
    unittest.main()
