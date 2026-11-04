# Changelog

## v0.2.0 (2026-11-04)

- **AI video support** — `client.video.generate(model, prompt)` submits a job, `client.video.status(task_id)` checks it, `client.video.wait(task_id)` polls until done (15 min default timeout, raises on upstream failure)
- Video routes: Kling, Seedance, Hailuo, Wan, Vidu (13 routes on the public rate card)
- Corrected catalog figures: 97 routes across 10 Chinese model families + international routes (was "48 models")
- `MODEL_REFERENCE.md` is now auto-generated from the live public pricing endpoint — regenerate with `python3 scripts/gen_model_reference.py` instead of editing by hand
- Package description updated to match the live catalog

## v0.1.0 (2026-06-20)

- Initial release
- OpenAI-compatible client (`aiwave.AIWave`)
- Support for 50+ Chinese AI models via one API key
- Chat completions with streaming support
- Environment variable configuration (`AIWAVE_API_KEY`)

[Get started →](https://aiwave.live)
