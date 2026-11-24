# Changelog

## Unreleased

## v0.2.2 (2026-11-24)

Documentation and metadata only. No runtime behaviour changes.

- State that the 13 video IDs are a subset of the 91 catalog IDs, not an additional set.
- Separate the OpenAI-compatible chat path from the experimental video path in the README introduction, and drop the claim that the client surfaces rates or usage evidence.
- Document how to set `AIWAVE_API_KEY` before running the examples.
- Stop the video example from hard-coding an API key string on a page that asks readers to keep keys out of source.
- Note that `kling-v2-6` is per-call while some Seedance IDs are token-priced, so `quota_type` has to be checked before estimating video spend.
- Fix `aiwave.__version__`, which still reported `0.2.0` in the published 0.2.1 release. It now tracks `pyproject.toml` again.
- `AGENTS.md` no longer hard-codes a model count. `/api/v1/pricing` is documented as the frozen 2026-10-24 51-row snapshot it actually is, not as a live source. The two endpoints share only 44 IDs.

## v0.2.1 (2026-11-13)

- Stop video polling near its requested timeout instead of sleeping a full interval past the deadline; use a monotonic clock for elapsed time.
- Recognize the generic and realtime video adapters' terminal status spellings so completed or failed jobs do not poll until timeout.
- Refuse invalid video polling intervals and timeouts before any status request; intervals shorter than one second can flood status checks.
- Reject an explicitly empty or invalid `api_key` rather than silently using an ambient `AIWAVE_API_KEY`. Omitting `api_key` still uses the AIWave environment key.
- Reject empty, whitespace-only, or non-string video prompts locally before sending a paid submission.
- Narrow package and client descriptions to supported operations; compatibility depends on the requested API operation.

## v0.2.0 (2026-11-04)

- **AI video support** — `client.video.generate(model, prompt)` submits a job, `client.video.status(task_id)` checks it, `client.video.wait(task_id)` polls until done (15 min default timeout, raises on upstream failure)
- Video catalog IDs: Kling, Seedance, Hailuo, Wan, Vidu (13 IDs on the public rate card; access and health vary by route and key)
- Corrected catalog figures: 97 model IDs on the public rate card across 10 Chinese families and other providers (was "48 models"); catalog presence does not prove route access or health
- `MODEL_REFERENCE.md` is now auto-generated from the live public pricing endpoint — regenerate with `python3 scripts/gen_model_reference.py` instead of editing by hand
- Package description updated to match the live catalog

## v0.1.0 (2026-06-20)

- Initial release
- OpenAI-compatible client (`aiwave.AIWave`)
- Support for 50+ Chinese AI models via one API key
- Chat completions with streaming support
- Environment variable configuration (`AIWAVE_API_KEY`)

[Get started →](https://aiwave.live)
