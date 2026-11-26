#!/usr/bin/env python3
"""Turn a media inventory JSON file into a concise Markdown handoff report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def format_duration(value: Any) -> str:
    if value is None:
        return "—"
    seconds = float(value)
    minutes, remainder = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{remainder:02d}" if hours else f"{minutes}:{remainder:02d}"


def markdown_report(records: list[dict[str, Any]], title: str) -> str:
    valid = [record for record in records if "error" not in record]
    errors = [record for record in records if "error" in record]
    lines = [f"# {title}", "", f"Assets: **{len(records)}**  ", f"Readable: **{len(valid)}**  ", f"Errors: **{len(errors)}**", ""]
    lines += ["| File | Duration | Video | Resolution | Audio |", "| --- | ---: | --- | ---: | --- |"]
    for record in valid:
        video = record.get("video", {})
        audio = record.get("audio", {})
        resolution = f"{video.get('width', '—')}×{video.get('height', '—')}"
        lines.append(
            f"| `{record.get('filename', record.get('file', 'unknown'))}` | "
            f"{format_duration(record.get('duration_seconds'))} | "
            f"{video.get('codec', '—')} | {resolution} | {audio.get('codec', '—')} |"
        )
    if errors:
        lines += ["", "## Files needing attention", ""]
        for record in errors:
            lines.append(f"- `{record.get('file', 'unknown')}`: {record['error']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert media inventory JSON to Markdown.")
    parser.add_argument("inventory", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--title", default="Media Asset Report")
    args = parser.parse_args()
    try:
        records = json.loads(args.inventory.read_text())
        report = markdown_report(records, args.title)
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(f"Could not read inventory: {exc}", file=sys.stderr)
        return 2
    if args.output:
        args.output.write_text(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
