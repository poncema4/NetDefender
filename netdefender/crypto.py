"""Cryptographic helpers for evidence integrity demonstrations."""

import hashlib
import hmac


def sha256_hex(data: bytes) -> str:
    """Return the SHA-256 digest of *data* as lowercase hexadecimal."""

    return hashlib.sha256(data).hexdigest()


def hmac_sha256_hex(data: bytes, secret: bytes) -> str:
    """Return an HMAC-SHA256 tag for *data* using *secret*."""

    return hmac.new(secret, data, hashlib.sha256).hexdigest()


def verify_hmac(data: bytes, secret: bytes, expected_hex: str) -> bool:
    """Verify an HMAC tag using a constant-time comparison."""

    actual = hmac_sha256_hex(data, secret)
    return hmac.compare_digest(actual, expected_hex)
