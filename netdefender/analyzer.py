"""Top-level analysis entry points for NetDefender."""

from collections.abc import Iterable

from .models import NetworkEvent


def analyze(events: Iterable[NetworkEvent]) -> list[NetworkEvent]:
    """Return normalized events for downstream detection.

    Detection and parsing are intentionally added in later phases. The
    Phase 1 implementation establishes a small, testable application
    boundary without pretending to detect attacks before evidence exists.
    """

    return list(events)
