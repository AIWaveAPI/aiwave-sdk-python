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
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

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


def render(models: list, pricing_version: str) -> str:
    version = str(pricing_version)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# AIWave Model Reference",
        "",
        f"**Auto-generated from the live public endpoint. Do not edit by hand.**",
        "",
        f"- Generated: {generated}",
        f"- Source: `{ENDPOINT}` (public, no key required)",
        f"- Pricing version: `{version[:16]}…`",
        f"- Models listed on public rate card: **{len(models)}**",
        "",
        "Regenerate with:",
        "",
        "```bash",
        "python3 scripts/gen_model_reference.py",
        "```",
        "",
        "Dated USD rates per model: https://aiwave.live/pricing",
        "Live availability: https://aiwave.live/models",
        "Request shape is not encoded in the pricing endpoint; check the model-specific docs before calling an API.",
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
        lines.append("| Model ID |")
        lines.append("|----------|")
        for m in sorted(items, key=lambda x: (x.get("model_name") or "").lower()):
            name = m.get("model_name") or m.get("id") or "?"
            lines.append(f"| `{name}` |")
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
    ap.add_argument("--check", action="store_true", help="compare the committed reference with the live endpoint")
    args = ap.parse_args()

    data = fetch()
    models = data.get("models") or data.get("data") or []
    if not models:
        print("ERROR: endpoint returned no models — refusing to write an empty reference.", file=sys.stderr)
        sys.exit(1)
    version = data.get("pricing_version")
    if not version:
        print("ERROR: endpoint returned no top-level pricing_version.", file=sys.stderr)
        sys.exit(1)

    out = render(models, pricing_version=version)
    if args.check:
        try:
            current = Path(args.out).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot read {args.out}: {exc}", file=sys.stderr)
            sys.exit(1)
        # Generated time is informational; the catalog content and source version must match.
        stable = lambda text: re.sub(r"(?m)^- Generated: .*\n", "- Generated: <ignored>\n", text)
        if stable(current) != stable(out):
            print(f"ERROR: {args.out} differs from the live catalog; regenerate it.", file=sys.stderr)
            sys.exit(1)
        print(f"PASS: {args.out} matches the live catalog ({len(models)} models)")
        return
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote {args.out}: {len(models)} models, generated {date.today().isoformat()}")


if __name__ == "__main__":
    main()
