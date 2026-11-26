#!/usr/bin/env python3
"""Inspect media files with ffprobe and emit stable JSON or CSV output."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def probe(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe was not found. Install FFmpeg and try again.")
    command = [
        "ffprobe", "-v", "error", "-show_format", "-show_streams",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        message = result.stderr.strip() or "ffprobe could not read the media file"
        raise RuntimeError(message)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    fmt = data.get("format", {})
    return {
        "file": str(path),
        "filename": path.name,
        "format": fmt.get("format_name"),
        "duration_seconds": _number(fmt.get("duration")),
        "size_bytes": _integer(fmt.get("size")),
        "bit_rate": _integer(fmt.get("bit_rate")),
        "video": {
            "codec": video.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "frame_rate": video.get("r_frame_rate"),
            "pixel_format": video.get("pix_fmt"),
        },
        "audio": {
            "codec": audio.get("codec_name"),
            "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"),
        },
    }


def _number(value: Any) -> float | None:
    try:
        return round(float(value), 3) if value is not None else None
    except (TypeError, ValueError):
        return None


def _integer(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect video/audio metadata using ffprobe.")
    parser.add_argument("files", nargs="+", type=Path, help="Media files to inspect")
    parser.add_argument("--csv", action="store_true", help="Emit a compact CSV report")
    args = parser.parse_args()
    records: list[dict[str, Any]] = []
    for path in args.files:
        try:
            records.append(probe(path))
        except (FileNotFoundError, RuntimeError, json.JSONDecodeError) as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            return 2
    if args.csv:
        fields = ["filename", "format", "duration_seconds", "size_bytes", "video_codec", "width", "height", "audio_codec"]
        writer = csv.DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        for item in records:
            writer.writerow({
                "filename": item["filename"], "format": item["format"],
                "duration_seconds": item["duration_seconds"], "size_bytes": item["size_bytes"],
                "video_codec": item["video"]["codec"], "width": item["video"]["width"],
                "height": item["video"]["height"], "audio_codec": item["audio"]["codec"],
            })
    else:
        json.dump(records, sys.stdout, indent=2)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
