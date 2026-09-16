"""Optional tshark adapter for turning a PCAP into NetDefender events."""

from __future__ import annotations

import csv
import io
import subprocess
from pathlib import Path

from .parser import parse_csv

FIELDS = (
    "frame.time_epoch",
    "ip.src",
    "ip.dst",
    "_ws.col.Protocol",
    "tcp.srcport",
    "tcp.dstport",
    "tcp.flags.str",
    "frame.len",
)


def pcap_to_csv(pcap: Path) -> str:
    """Export useful packet fields from a PCAP using installed tshark."""
    command = ["tshark", "-r", str(pcap), "-T", "fields", "-E", "header=y", "-E", "separator=,", "-E", "quote=d"]
    for field in FIELDS:
        command.extend(("-e", field))
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    reader = csv.DictReader(io.StringIO(result.stdout))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp", "source_ip", "destination_ip", "protocol", "source_port", "destination_port", "tcp_flags", "packet_length"])
    writer.writeheader()
    for row in reader:
        writer.writerow({
            "timestamp": row.get("frame.time_epoch", ""),
            "source_ip": row.get("ip.src", ""),
            "destination_ip": row.get("ip.dst", ""),
            "protocol": row.get("_ws.col.Protocol", "UNKNOWN"),
            "source_port": row.get("tcp.srcport", ""),
            "destination_port": row.get("tcp.dstport", ""),
            "tcp_flags": row.get("tcp.flags.str", ""),
            "packet_length": row.get("frame.len", ""),
        })
    return output.getvalue()


def parse_pcap(pcap: Path):
    """Parse a PCAP through tshark into NetDefender NetworkEvent objects."""
    return parse_csv(pcap_to_csv(pcap))
