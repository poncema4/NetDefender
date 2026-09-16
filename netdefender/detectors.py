"""Detection rules for controlled network reconnaissance."""

from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from .models import Finding, NetworkEvent


def detect_syn_scan(events: list[NetworkEvent], *, min_distinct_ports: int = 10, window_seconds: int = 10) -> list[Finding]:
    """Detect a burst of TCP SYNs from one source to many ports on one target."""
    syns = [
        e for e in events
        if e.protocol == "TCP"
        and e.destination_port is not None
        and e.tcp_flags is not None
        and "SYN" in e.tcp_flags
        and "ACK" not in e.tcp_flags
    ]
    groups: dict[tuple[str, str], list[NetworkEvent]] = defaultdict(list)
    for event in syns:
        groups[(event.source_ip, event.destination_ip)].append(event)

    findings: list[Finding] = []
    window = timedelta(seconds=window_seconds)
    for (source, target), group in groups.items():
        group.sort(key=lambda e: e.timestamp)
        for start_index, start in enumerate(group):
            window_events = [e for e in group[start_index:] if e.timestamp - start.timestamp <= window]
            ports = sorted({e.destination_port for e in window_events if e.destination_port is not None})
            if len(ports) >= min_distinct_ports:
                findings.append(Finding(
                    rule_id="NET-RECON-001",
                    title="TCP SYN reconnaissance pattern detected",
                    severity="medium",
                    source_ip=source,
                    destination_ip=target,
                    evidence={
                        "distinct_destination_ports": ports,
                        "packet_count": len(window_events),
                        "window_seconds": window_seconds,
                    },
                ))
                break
    return findings


def detect(events: list[NetworkEvent]) -> list[Finding]:
    """Run all enabled NetDefender detection rules."""
    return detect_syn_scan(events)
