# Media Inspector CLI

[![CI](https://github.com/mdeyasin780/dev-video-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/mdeyasin780/dev-video-toolkit/actions/workflows/ci.yml)

A small, original developer utility for video editors: inspect one or more media files with `ffprobe` and export a stable JSON or CSV report for asset tracking and batch workflows.

## Features

- Reports container format, duration, size, bitrate, video and audio streams.
- Supports multiple files in one command.
- Emits JSON by default and compact CSV with `--csv`.
- Keeps the core implementation dependency-free; only FFmpeg/`ffprobe` is required.

## Recursive asset inventory

For a footage folder, `media_inventory.py` scans nested directories and creates a machine-readable inventory. This is useful for editor hand-offs, batch review, and automation or agent workflows.

```bash
python3 media_inventory.py ./footage > footage-inventory.json
python3 media_inventory.py ./footage --extensions mp4 mov webm > footage-inventory.json
```

Unreadable media is recorded with an `error` field instead of stopping the entire inventory run.

## Compare two inventory snapshots

Use `media_diff.py` to identify new, removed, changed, and unchanged assets between two scans. Compare snapshots generated from the same footage root so their `file` paths remain stable.

```bash
python3 media_inventory.py ./footage > inventory-before.json
# Add, remove, or replace footage, then scan again.
python3 media_inventory.py ./footage > inventory-after.json
python3 media_diff.py inventory-before.json inventory-after.json -o inventory-diff.json
```

The diff output contains a summary plus the full before/after records for changed assets. This makes it suitable for editor handoffs, review checklists, and automated pipeline decisions.

## Markdown handoff report

Turn an inventory into a concise report for a client, editor, or issue tracker:

```bash
python3 media_report.py footage-inventory.json --title "Monday Footage" -o footage-report.md
```

The report includes asset counts, duration, codecs, resolution, and a separate section for files that need attention.

## Requirements

- Python 3.10+
- FFmpeg installed and available as `ffprobe` on `PATH`

## Usage

```bash
python3 media_inspector.py input.mp4
python3 media_inspector.py clips/*.mov --csv > media-report.csv
```

## Development and CI

Run the same checks locally that GitHub Actions runs automatically on every push and pull request:

```bash
python3 -m compileall -q media_inspector.py media_inventory.py media_report.py media_diff.py tests
python3 -m unittest discover -s tests -v
```

The CI workflow tests Python 3.10 through 3.13. See [CHANGELOG.md](CHANGELOG.md) for project history.

## License and provenance

This repository is an original implementation created for the repository owner. It is released under the MIT License. It does not copy code, assets, or documentation from the existing `ETFinix-Tool` repository. The tool delegates media parsing to the separately installed FFmpeg project; FFmpeg remains under its own license.
