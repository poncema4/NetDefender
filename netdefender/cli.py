"""Command-line interface for NetDefender."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze, findings_to_json
from .parser import parse_csv, parse_json
from .report import render_html


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze controlled network-security evidence.")
    parser.add_argument("input", type=Path, help="JSON or CSV event file")
    parser.add_argument("--format", choices=("json", "csv"), help="Input format; inferred from extension when omitted")
    parser.add_argument("--html", type=Path, help="Also write an HTML security report")
    args = parser.parse_args()

    fmt = args.format or args.input.suffix.lower().lstrip(".")
    text = args.input.read_text(encoding="utf-8")
    if fmt == "json":
        events = parse_json(text)
    elif fmt == "csv":
        events = parse_csv(text)
    else:
        parser.error("input format must be JSON or CSV")

    findings = analyze(events)
    print(findings_to_json(findings))
    if args.html:
        args.html.write_text(render_html(findings), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
