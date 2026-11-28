#!/usr/bin/env python3
"""Compare two media inventory JSON files and report asset changes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def asset_id(record: dict[str, Any]) -> str:
    """Return the stable identifier used to compare records across inventories."""
    return str(record.get("file") or record.get("filename") or "")


def fingerprint(record: dict[str, Any]) -> str:
    """Serialize meaningful metadata so ordering does not create false changes."""
    comparable = {key: value for key, value in record.items() if key != "file"}
    return json.dumps(comparable, sort_keys=True, separators=(",", ":"))


def diff_manifests(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, Any]:
    old = {asset_id(record): record for record in before if asset_id(record)}
    new = {asset_id(record): record for record in after if asset_id(record)}
    added_ids = sorted(set(new) - set(old))
    removed_ids = sorted(set(old) - set(new))
    changed_ids = sorted(key for key in set(old) & set(new) if fingerprint(old[key]) != fingerprint(new[key]))
    unchanged = len(set(old) & set(new)) - len(changed_ids)
    return {
        "summary": {
            "added": len(added_ids),
            "removed": len(removed_ids),
            "changed": len(changed_ids),
            "unchanged": unchanged,
        },
        "added": [new[key] for key in added_ids],
        "removed": [old[key] for key in removed_ids],
        "changed": [{"before": old[key], "after": new[key]} for key in changed_ids],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two media inventory JSON files.")
    parser.add_argument("before", type=Path, help="Earlier inventory JSON")
    parser.add_argument("after", type=Path, help="Newer inventory JSON")
    parser.add_argument("-o", "--output", type=Path, help="Write the diff JSON to a file")
    args = parser.parse_args()
    try:
        before = json.loads(args.before.read_text())
        after = json.loads(args.after.read_text())
        result = diff_manifests(before, after)
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(f"Could not compare inventories: {exc}", file=sys.stderr)
        return 2
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
