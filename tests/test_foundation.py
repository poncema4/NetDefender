from datetime import datetime, timezone

from netdefender.analyzer import analyze
from netdefender.crypto import hmac_sha256_hex, sha256_hex, verify_hmac
from netdefender.detectors import detect
from netdefender.models import NetworkEvent


def test_single_network_event_is_not_a_detection_by_itself() -> None:
    event = NetworkEvent(
        timestamp=datetime.now(timezone.utc),
        source_ip="10.10.10.10",
        destination_ip="10.10.10.20",
        protocol="TCP",
        source_port=40000,
        destination_port=80,
        tcp_flags="SYN",
    )

    # The analyzer returns security findings, not raw events. A single SYN
    # packet is intentionally below the reconnaissance detection threshold.
    assert analyze([event]) == []


def test_detector_returns_no_findings_for_empty_input() -> None:
    assert detect([]) == []


def test_sha256_is_deterministic() -> None:
    assert sha256_hex(b"netdefender") == sha256_hex(b"netdefender")
    assert sha256_hex(b"netdefender") != sha256_hex(b"modified")


def test_hmac_can_be_verified_and_detects_tampering() -> None:
    data = b"controlled evidence"
    secret = b"phase-one-test-secret"
    tag = hmac_sha256_hex(data, secret)

    assert verify_hmac(data, secret, tag)
    assert not verify_hmac(b"modified evidence", secret, tag)
