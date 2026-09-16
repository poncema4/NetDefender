"""Parsers for NetDefender network-event input."""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from typing import Any, Iterable

from .models import NetworkEvent


def _timestamp(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _int(value: str | int | None) -> int | None:
    if value in (None, "", "-"):
        return None
    return int(value)


def event_from_mapping(row: dict[str, Any]) -> NetworkEvent:
    """Convert a JSON/CSV-style mapping into a normalized event."""
    return NetworkEvent(
        timestamp=_timestamp(str(row.get("timestamp", ""))),
        source_ip=str(row["source_ip"]),
        destination_ip=str(row["destination_ip"]),
        protocol=str(row.get("protocol", "UNKNOWN")).upper(),
        source_port=_int(row.get("source_port")),
        destination_port=_int(row.get("destination_port")),
        tcp_flags=(str(row["tcp_flags"]).upper() if row.get("tcp_flags") else None),
        packet_length=_int(row.get("packet_length")),
    )


def parse_json(text: str) -> list[NetworkEvent]:
    """Parse a JSON array of normalized network events."""
    payload = json.loads(text)
    if not isinstance(payload, list):
        raise ValueError("JSON input must contain an array of events")
    return [event_from_mapping(item) for item in payload]


def parse_csv(text: str) -> list[NetworkEvent]:
    """Parse CSV with NetDefender event field names."""
    reader = csv.DictReader(io.StringIO(text))
    required = {"timestamp", "source_ip", "destination_ip", "protocol"}
    if not required.issubset(reader.fieldnames or set()):
        raise ValueError(f"CSV must contain: {', '.join(sorted(required))}")
    return [event_from_mapping(row) for row in reader]


def parse_rows(rows: Iterable[dict[str, Any]]) -> list[NetworkEvent]:
    return [event_from_mapping(row) for row in rows]
