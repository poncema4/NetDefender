"""Analysis pipeline for NetDefender."""

from __future__ import annotations

import json
from collections.abc import Iterable

from .detectors import detect
from .models import Finding, NetworkEvent


def analyze(events: Iterable[NetworkEvent]) -> list[Finding]:
    """Run the detection engine over normalized network events."""
    return detect(list(events))


def findings_to_json(findings: Iterable[Finding]) -> str:
    """Serialize findings into stable, human-readable JSON."""
    return json.dumps([
        {
            "rule_id": f.rule_id,
            "title": f.title,
            "severity": f.severity,
            "source_ip": f.source_ip,
            "destination_ip": f.destination_ip,
            "evidence": f.evidence,
        }
        for f in findings
    ], indent=2, sort_keys=True)
