"""Command-line interface for NetDefender."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze, findings_to_json
from .parser import parse_csv, parse_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze controlled network-security evidence.")
    parser.add_argument("input", type=Path, help="JSON or CSV event file")
    parser.add_argument("--format", choices=("json", "csv"), help="Input format; inferred from extension when omitted")
    args = parser.parse_args()

    fmt = args.format or args.input.suffix.lower().lstrip(".")
    text = args.input.read_text(encoding="utf-8")
    events = parse_json(text) if fmt == "json" else parse_csv(text) if fmt == "csv" else None
    if events is None:
        parser.error("input format must be JSON or CSV")

    findings = analyze(events)
    print(findings_to_json(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
