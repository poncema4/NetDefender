"""Core data models for normalized network observations."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NetworkEvent:
    """A normalized observation of network traffic.

    Later phases will populate these objects from packet captures or
    structured exports. Keeping a stable model makes detection rules
    independent from the original capture format.
    """

    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int | None = None
    destination_port: int | None = None
    tcp_flags: str | None = None
