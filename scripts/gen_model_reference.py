#!/usr/bin/env python3
"""Generate MODEL_REFERENCE.md from the live public pricing endpoint.

Usage:
    python3 scripts/gen_model_reference.py [--out MODEL_REFERENCE.md]

Pulls https://aiwave.live/api/pricing (public, no key), groups models by
family, and writes a dated reference table. Re-run before every release so
the doc never goes stale (the previous hand-written version listed models
that have been retired).

Verification: run scripts/verify_claims.py — this generator and that checker
read the same endpoint. If claims pass, the reference is current.
"""
import argparse
import json
import sys
import urllib.request
from datetime import date, datetime, timezone

ENDPOINT = "https://aiwave.live/api/pricing"

FAMILY_PREFIXES = [
    ("DeepSeek", ["deepseek"]),
    ("GLM (Zhipu)", ["glm"]),
    ("Kimi (Moonshot)", ["kimi"]),
    ("Qwen (Alibaba)", ["qwen"]),
    ("Doubao (ByteDance)", ["doubao"]),
    ("StepFun", ["step"]),
    ("Xiaomi MiMo", ["xiaomi"]),
    ("MiniMax", ["minimax"]),
    ("Video — Kling (Kuaishou)", ["kling"]),
    ("Video — Wan (Alibaba)", ["wan3"]),
    ("Claude (coding-team)", ["claude"]),
    ("International", ["gpt", "gemini", "cohere", "nvidia", "happyhorse", "inclusionai"]),
]


def fetch():
    req = urllib.request.Request(ENDPOINT, headers={"User-Agent": "aiwave-genref/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def family_of(model_name: str) -> str:
    n = model_name.lower()
    for label, prefixes in FAMILY_PREFIXES:
        for p in prefixes:
            if n.startswith(p):
                return label
    return "Other"


def is_video(model_name: str) -> bool:
    n = model_name.lower()
    return any(k in n for k in ("kling", "seedance", "hailuo", "wan3.0-video", "vidu"))


def render(models: list) -> str:
    version = str(models[0].get("pricing_version", "unknown")) if models else "unknown"
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# AIWave Model Reference",
        "",
        f"**Auto-generated from the live public endpoint. Do not edit by hand.**",
        "",
        f"- Generated: {generated}",
        f"- Source: `{ENDPOINT}` (public, no key required)",
        f"- Pricing version: `{version[:16]}…`",
        f"- Routes on the public rate card: **{len(models)}**",
        "",
        "Regenerate with:",
        "",
        "```bash",
        "python3 scripts/gen_model_reference.py",
        "```",
        "",
        "Dated USD rates per model: https://aiwave.live/pricing",
        "Live availability: https://aiwave.live/models",
        "",
        "---",
        "",
    ]

    groups: dict[str, list] = {}
    for m in models:
        name = m.get("model_name") or m.get("id") or "?"
        groups.setdefault(family_of(name), []).append(m)

    for label, _ in FAMILY_PREFIXES + [("Other", [])]:
        items = groups.get(label)
        if not items:
            continue
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| Model ID | Kind |")
        lines.append("|----------|------|")
        for m in sorted(items, key=lambda x: (x.get("model_name") or "").lower()):
            name = m.get("model_name") or m.get("id") or "?"
            kind = "video generation" if is_video(name) else "chat / reasoning"
            lines.append(f"| `{name}` | {kind} |")
        lines.append("")

    lines += [
        "---",
        "",
        "This table lists model IDs only. Rates change as vendors update",
        "pricing — always confirm current numbers at https://aiwave.live/pricing",
        "or via the endpoint above.",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="MODEL_REFERENCE.md")
    args = ap.parse_args()

    data = fetch()
    models = data.get("models") or data.get("data") or []
    if not models:
        print("ERROR: endpoint returned no models — refusing to write an empty reference.", file=sys.stderr)
        sys.exit(1)

    out = render(models)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote {args.out}: {len(models)} routes, generated {date.today().isoformat()}")


if __name__ == "__main__":
    main()
