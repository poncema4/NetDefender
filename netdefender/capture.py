"""Optional tshark adapter for turning a PCAP into NetDefender events."""

from __future__ import annotations

import csv
import io
import subprocess
from pathlib import Path

from .parser import parse_csv

# Use protocol numbers instead of Wireshark's display-column field. The latter
# can be empty depending on TShark's protocol-column rendering/version.
FIELDS = (
    "frame.time_epoch",
    "ip.src",
    "ip.dst",
    "ip.proto",
    "tcp.srcport",
    "tcp.dstport",
    "tcp.flags",
    "frame.len",
)

_IP_PROTOCOLS = {
    "1": "ICMP",
    "6": "TCP",
    "17": "UDP",
}

_TCP_FLAG_BITS = (
    (0x001, "FIN"),
    (0x002, "SYN"),
    (0x004, "RST"),
    (0x008, "PSH"),
    (0x010, "ACK"),
    (0x020, "URG"),
    (0x040, "ECE"),
    (0x080, "CWR"),
    (0x100, "NS"),
)


def normalize_protocol(value: str | None) -> str:
    """Normalize TShark's IP protocol number into an application protocol name."""
    if not value:
        return "UNKNOWN"

    normalized = value.strip().upper()
    if normalized in _IP_PROTOCOLS:
        return _IP_PROTOCOLS[normalized]

    # Keep compatibility with callers/tests that already provide protocol names.
    if normalized in _IP_PROTOCOLS.values():
        return normalized

    return normalized


def normalize_tcp_flags(value: str | None) -> str:
    """Normalize tshark's numeric TCP flag bitmask into stable flag names."""
    if not value:
        return ""

    try:
        flags = int(value, 0)
    except ValueError:
        # Keep compatibility with already-normalized/test fixture values.
        return value

    return ",".join(name for bit, name in _TCP_FLAG_BITS if flags & bit)


def pcap_to_csv(pcap: Path) -> str:
    """Export useful packet fields from a PCAP using installed tshark."""
    command = [
        "tshark",
        "-r",
        str(pcap),
        "-T",
        "fields",
        "-E",
        "header=y",
        "-E",
        "separator=,",
        "-E",
        "quote=d",
    ]
    for field in FIELDS:
        command.extend(("-e", field))
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    reader = csv.DictReader(io.StringIO(result.stdout))
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "timestamp",
            "source_ip",
            "destination_ip",
            "protocol",
            "source_port",
            "destination_port",
            "tcp_flags",
            "packet_length",
        ],
    )
    writer.writeheader()
    for row in reader:
        writer.writerow(
            {
                "timestamp": row.get("frame.time_epoch", ""),
                "source_ip": row.get("ip.src", ""),
                "destination_ip": row.get("ip.dst", ""),
                "protocol": normalize_protocol(row.get("ip.proto", "")),
                "source_port": row.get("tcp.srcport", ""),
                "destination_port": row.get("tcp.dstport", ""),
                "tcp_flags": normalize_tcp_flags(row.get("tcp.flags", "")),
                "packet_length": row.get("frame.len", ""),
            }
        )
    return output.getvalue()


def parse_pcap(pcap: Path):
    """Parse a PCAP through tshark into NetDefender NetworkEvent objects."""
    return parse_csv(pcap_to_csv(pcap))
