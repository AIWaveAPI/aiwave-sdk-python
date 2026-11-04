"""The pricing endpoint must not be treated as a route capability source."""

import importlib.util
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "model_reference", Path(__file__).with_name("gen_model_reference.py")
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class ModelReferenceTests(unittest.TestCase):
    def test_unknown_request_shapes_are_not_labeled_chat(self):
        models = [
            {"model_name": "qwen-audio-3.0-realtime-flash", "pricing_version": "fixture"},
            {"model_name": "qwen-image-3.0", "pricing_version": "fixture"},
            {"model_name": "qwen3.7-text-embedding", "pricing_version": "fixture"},
            {"model_name": "deepseek-v4-pro", "pricing_version": "fixture"},
        ]
        reference = generator.render(models, pricing_version="fixture")
        self.assertIn("Models listed on public rate card", reference)
        self.assertNotIn("chat / reasoning", reference)
        self.assertNotIn("| Kind |", reference)
        for model in models:
            self.assertEqual(reference.count("`" + model["model_name"] + "`"), 1)
        self.assertIn("Request shape", reference)

    def test_reference_uses_top_level_pricing_version(self):
        models = [{"model_name": "deepseek-v4-pro", "pricing_version": "old-row-version"}]
        reference = generator.render(models, pricing_version="new-top-level-version")
        self.assertIn("new-top-level", reference)
        self.assertNotIn("old-row-version", reference)


if __name__ == "__main__":
    unittest.main()
