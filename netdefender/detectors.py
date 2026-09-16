"""Detection rules for controlled network reconnaissance."""

from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from .models import Finding, NetworkEvent


def _group_in_window(events: list[NetworkEvent], window_seconds: int) -> list[list[NetworkEvent]]:
    window = timedelta(seconds=window_seconds)
    ordered = sorted(events, key=lambda e: e.timestamp)
    groups: list[list[NetworkEvent]] = []
    for index, start in enumerate(ordered):
        current = [e for e in ordered[index:] if e.timestamp - start.timestamp <= window]
        groups.append(current)
    return groups


def detect_syn_scan(events: list[NetworkEvent], *, min_distinct_ports: int = 10, window_seconds: int = 10) -> list[Finding]:
    """Detect a burst of TCP SYNs from one source to many target ports."""
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
    for (source, target), group in groups.items():
        for window_events in _group_in_window(group, window_seconds):
            ports = sorted({e.destination_port for e in window_events if e.destination_port is not None})
            if len(ports) >= min_distinct_ports:
                findings.append(Finding(
                    rule_id="NET-RECON-001",
                    title="TCP SYN reconnaissance pattern detected",
                    severity="medium",
                    source_ip=source,
                    destination_ip=target,
                    evidence={"distinct_destination_ports": ports, "packet_count": len(window_events), "window_seconds": window_seconds},
                ))
                break
    return findings


def detect_udp_scan(events: list[NetworkEvent], *, min_distinct_ports: int = 8, window_seconds: int = 10) -> list[Finding]:
    """Detect a burst of UDP probes to many target ports."""
    udp = [e for e in events if e.protocol == "UDP" and e.destination_port is not None]
    groups: dict[tuple[str, str], list[NetworkEvent]] = defaultdict(list)
    for event in udp:
        groups[(event.source_ip, event.destination_ip)].append(event)

    findings: list[Finding] = []
    for (source, target), group in groups.items():
        for window_events in _group_in_window(group, window_seconds):
            ports = sorted({e.destination_port for e in window_events if e.destination_port is not None})
            if len(ports) >= min_distinct_ports:
                findings.append(Finding(
                    rule_id="NET-RECON-002",
                    title="UDP reconnaissance pattern detected",
                    severity="medium",
                    source_ip=source,
                    destination_ip=target,
                    evidence={"distinct_destination_ports": ports, "packet_count": len(window_events), "window_seconds": window_seconds},
                ))
                break
    return findings


def detect(events: list[NetworkEvent]) -> list[Finding]:
    """Run all enabled NetDefender reconnaissance rules."""
    return detect_syn_scan(events) + detect_udp_scan(events)
