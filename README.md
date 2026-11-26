# Media Inspector CLI

A small, original developer utility for video editors: inspect one or more media files with `ffprobe` and export a stable JSON or CSV report for asset tracking and batch workflows.

## Features

- Reports container format, duration, size, bitrate, video and audio streams.
- Supports multiple files in one command.
- Emits JSON by default and compact CSV with `--csv`.
- Keeps the core implementation dependency-free; only FFmpeg/`ffprobe` is required.

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
