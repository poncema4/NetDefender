"""Core data models for NetDefender."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class NetworkEvent:
    """Normalized observation of one network packet/event."""

    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int | None = None
    destination_port: int | None = None
    tcp_flags: str | None = None
    packet_length: int | None = None


@dataclass(frozen=True)
class Finding:
    """Explainable security finding produced by a detection rule."""

    rule_id: str
    title: str
    severity: str
    source_ip: str
    destination_ip: str
    evidence: dict[str, Any] = field(default_factory=dict)
