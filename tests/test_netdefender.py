from datetime import datetime, timezone

from netdefender.analyzer import analyze
from netdefender.crypto import hmac_sha256_hex, sha256_hex, verify_hmac
from netdefender.models import NetworkEvent
from netdefender.parser import parse_json


def event(port: int, second: int = 0, flags: str = "SYN") -> NetworkEvent:
    return NetworkEvent(
        timestamp=datetime(2026, 1, 1, 12, 0, second, tzinfo=timezone.utc),
        source_ip="192.0.2.10",
        destination_ip="192.0.2.20",
        protocol="TCP",
        source_port=40000 + port,
        destination_port=port,
        tcp_flags=flags,
    )


def test_syn_scan_is_detected():
    findings = analyze([event(port) for port in range(20, 32)])
    assert len(findings) == 1
    assert findings[0].rule_id == "NET-RECON-001"
    assert findings[0].severity == "medium"


def test_small_number_of_ports_is_not_detected():
    findings = analyze([event(port) for port in range(20, 25)])
    assert findings == []


def test_ack_packets_are_not_treated_as_syn_scan():
    findings = analyze([event(port, flags="SYN,ACK") for port in range(20, 40)])
    assert findings == []


def test_json_parser():
    events = parse_json('[{"timestamp":"2026-01-01T12:00:00Z","source_ip":"192.0.2.10","destination_ip":"192.0.2.20","protocol":"TCP","destination_port":22,"tcp_flags":"SYN"}]')
    assert len(events) == 1
    assert events[0].destination_port == 22


def test_crypto_integrity():
    data = b"controlled packet evidence"
    secret = b"test-only-secret"
    digest = sha256_hex(data)
    tag = hmac_sha256_hex(data, secret)
    assert len(digest) == 64
    assert verify_hmac(data, secret, tag)
    assert not verify_hmac(data + b"tampered", secret, tag)
