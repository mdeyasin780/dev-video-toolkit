#!/usr/bin/env python3
"""Build a machine-readable inventory for a directory of media assets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from media_inspector import probe

DEFAULT_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mp3", ".wav", ".flac", ".aac"}


def inventory(root: Path, extensions: set[str]) -> list[dict]:
    if not root.is_dir():
        raise NotADirectoryError(root)
    records = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            try:
                records.append(probe(path))
            except (RuntimeError, json.JSONDecodeError) as exc:
                records.append({"file": str(path), "error": str(exc)})
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory media assets recursively.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--extensions", nargs="+", help="Extensions without or with dots, e.g. mp4 mov")
    args = parser.parse_args()
    extensions = {f".{item.lstrip('.').lower()}" for item in args.extensions} if args.extensions else DEFAULT_EXTENSIONS
    try:
        json.dump(inventory(args.directory, extensions), sys.stdout, indent=2)
        print()
    except NotADirectoryError as exc:
        print(f"{exc}: not a directory", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
