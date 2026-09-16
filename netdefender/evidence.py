"""Cryptographic evidence packaging helpers."""

from __future__ import annotations

import json
from dataclasses import asdict

from .crypto import hmac_sha256_hex, sha256_hex, verify_hmac
from .models import Finding


def build_manifest(findings: list[Finding], evidence_bytes: bytes, secret: bytes) -> dict[str, object]:
    """Create a compact integrity manifest for a finding/evidence artifact."""
    digest = sha256_hex(evidence_bytes)
    return {
        "schema_version": 1,
        "evidence_sha256": digest,
        "evidence_hmac_sha256": hmac_sha256_hex(evidence_bytes, secret),
        "finding_count": len(findings),
        "findings": [asdict(f) for f in findings],
    }


def verify_manifest(evidence_bytes: bytes, manifest: dict[str, object], secret: bytes) -> bool:
    """Verify both the SHA-256 digest and HMAC recorded in a manifest."""
    expected_digest = str(manifest.get("evidence_sha256", ""))
    expected_hmac = str(manifest.get("evidence_hmac_sha256", ""))
    return sha256_hex(evidence_bytes) == expected_digest and verify_hmac(
        evidence_bytes, secret, expected_hmac
    )


def manifest_json(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True)
