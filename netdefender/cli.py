"""Command-line interface for NetDefender."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze, findings_to_json
from .capture import parse_pcap
from .parser import parse_csv, parse_json
from .report import render_html


def load_events(path: Path, fmt: str | None):
    detected = fmt or path.suffix.lower().lstrip(".")
    if detected == "json":
        return parse_json(path.read_text(encoding="utf-8"))
    if detected == "csv":
        return parse_csv(path.read_text(encoding="utf-8"))
    if detected in {"pcap", "pcapng"}:
        return parse_pcap(path)
    raise ValueError("input format must be JSON, CSV, PCAP, or PCAPNG")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze controlled network-security evidence.")
    parser.add_argument("input", type=Path, help="JSON, CSV, PCAP, or PCAPNG evidence file")
    parser.add_argument("--format", choices=("json", "csv", "pcap"), help="Input format; inferred from extension when omitted")
    parser.add_argument("--html", type=Path, help="Also write an HTML security report")
    args = parser.parse_args()

    try:
        events = load_events(args.input, args.format)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    findings = analyze(events)
    print(findings_to_json(findings))
    if args.html:
        args.html.write_text(render_html(findings), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
