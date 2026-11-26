# Media Inspector CLI

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

## Requirements

- Python 3.10+
- FFmpeg installed and available as `ffprobe` on `PATH`

## Usage

```bash
python3 media_inspector.py input.mp4
python3 media_inspector.py clips/*.mov --csv > media-report.csv
```

## Development

```bash
python3 -m unittest discover -s tests -v
```

## License and provenance

This repository is an original implementation created for the repository owner. It is released under the MIT License. It does not copy code, assets, or documentation from the existing `ETFinix-Tool` repository. The tool delegates media parsing to the separately installed FFmpeg project; FFmpeg remains under its own license.
