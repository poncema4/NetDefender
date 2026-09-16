"""Detection rules for NetDefender."""

from .models import NetworkEvent


def detect(events: list[NetworkEvent]) -> list[dict[str, object]]:
    """Run enabled detection rules.

    Phase 1 intentionally returns no findings. Reconnaissance detection is
    implemented and tested in later phases after real lab evidence exists.
    """

    _ = events
    return []
