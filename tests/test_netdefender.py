from datetime import datetime, timezone

from netdefender.analyzer import analyze
from netdefender.capture import normalize_tcp_flags
from netdefender.crypto import hmac_sha256_hex, sha256_hex, verify_hmac
from netdefender.evidence import build_manifest, verify_manifest
from netdefender.models import NetworkEvent
from netdefender.parser import parse_json
from netdefender.report import render_html


def event(port: int, second: int = 0, flags: str = "SYN", protocol: str = "TCP") -> NetworkEvent:
    return NetworkEvent(
        timestamp=datetime(2026, 1, 1, 12, 0, second, tzinfo=timezone.utc),
        source_ip="192.0.2.10",
        destination_ip="192.0.2.20",
        protocol=protocol,
        source_port=40000 + port,
        destination_port=port,
        tcp_flags=flags,
    )


def test_syn_scan_is_detected():
    findings = analyze([event(port) for port in range(20, 32)])
    assert len(findings) == 1
    assert findings[0].rule_id == "NET-RECON-001"


def test_small_number_of_ports_is_not_detected():
    assert analyze([event(port) for port in range(20, 25)]) == []


def test_ack_packets_are_not_treated_as_syn_scan():
    assert analyze([event(port, flags="SYN,ACK") for port in range(20, 40)]) == []


def test_udp_scan_is_detected():
    findings = analyze([event(port, protocol="UDP", flags=None) for port in range(30, 38)])
    assert len(findings) == 1
    assert findings[0].rule_id == "NET-RECON-002"


def test_tshark_numeric_tcp_flags_are_normalized():
    assert normalize_tcp_flags("0x0002") == "SYN"
    assert normalize_tcp_flags("0x0012") == "SYN,ACK"
    assert normalize_tcp_flags("0x001") == "FIN"
    assert normalize_tcp_flags("SYN") == "SYN"
    assert normalize_tcp_flags("") == ""


def test_json_parser():
    events = parse_json('[{"timestamp":"2026-01-01T12:00:00Z","source_ip":"192.0.2.10","destination_ip":"192.0.2.20","protocol":"TCP","destination_port":22,"tcp_flags":"SYN"}]')
    assert events[0].destination_port == 22


def test_crypto_integrity():
    data = b"controlled packet evidence"
    secret = b"test-only-secret"
    digest = sha256_hex(data)
    tag = hmac_sha256_hex(data, secret)
    assert len(digest) == 64
    assert verify_hmac(data, secret, tag)
    assert not verify_hmac(data + b"tampered", secret, tag)


def test_evidence_manifest_detects_tampering():
    data = b"controlled packet evidence"
    secret = b"test-only-secret"
    findings = analyze([event(port) for port in range(20, 32)])
    manifest = build_manifest(findings, data, secret)
    assert verify_manifest(data, manifest, secret)
    assert not verify_manifest(data + b"tampered", manifest, secret)


def test_html_report_contains_finding():
    html = render_html(analyze([event(port) for port in range(20, 32)]))
    assert "TCP SYN reconnaissance pattern detected" in html
    assert "NET-RECON-001" in html
