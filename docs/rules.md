# NetDefender Detection Rules

This document defines the supported detection behavior and the engineering requirements that keep NetDefender deterministic, explainable, safe, and reproducible.

## Detection Rules

| Rule | Name | Trigger | Default threshold | Severity |
|---|---|---|---|---|
| `NET-RECON-001` | TCP SYN reconnaissance | One source sends TCP SYN probes to many destination ports on one target within a short window | 10 distinct ports / 10 seconds | Medium |
| `NET-RECON-002` | UDP reconnaissance | One source sends UDP probes to many destination ports on one target within a short window | 8 distinct ports / 10 seconds | Medium |

### NET-RECON-001 — TCP SYN Reconnaissance

The rule evaluates TCP events where:

- protocol is `TCP`;
- a destination port is present;
- TCP flags contain `SYN`;
- TCP flags do not contain `ACK`;
- the same source/target pair contacts at least 10 distinct destination ports;
- the observations occur within a 10-second window.

The validated Nmap experiment used:

```bash
sudo nmap -sS -p 1-100 172.16.198.128
```

and produced a `NET-RECON-001` finding from the captured traffic.

### NET-RECON-002 — UDP Reconnaissance

The rule evaluates UDP events where:

- protocol is `UDP`;
- a destination port is present;
- the same source/target pair contacts at least 8 distinct destination ports;
- the observations occur within a 10-second window.

The validated Nmap experiment used:

```bash
sudo nmap -sU -p 1-20 172.16.198.128
```

and produced a `NET-RECON-002` finding from the captured traffic.

## Finding Semantics

A finding means the observed event set matched a documented NetDefender condition.

It does not automatically mean:

- the source is malicious;
- compromise occurred;
- an attack succeeded;
- the source's intent is known;
- the rule detects every scan.

Controlled experiments, authorized vulnerability scanning, monitoring, and legitimate testing can all generate reconnaissance-like traffic.

## Detection Design Requirements

Every supported detection rule should:

1. Have a unique `NET-*` identifier.
2. State the event fields it consumes.
3. Use explicit thresholds.
4. Produce explainable evidence.
5. Have positive tests.
6. Have negative tests for important non-detections.
7. Be deterministic for the same input.
8. Avoid wall-clock dependence during analysis.
9. Avoid external services.
10. Be documented before becoming part of the supported detection contract.

## Input and Normalization Rules

Supported inputs are:

- JSON normalized events;
- CSV normalized events;
- PCAP/PCAPNG through the TShark adapter.

All inputs become `NetworkEvent` objects before detection.

Detection rules must not contain format-specific parsing logic.

For real PCAP input, the adapter normalizes:

- IPv4 addresses;
- IP protocol values;
- TCP flags;
- TCP/UDP transport ports;
- timestamps;
- packet length.

## Evidence Rules

A finding should contain enough information to explain why the rule fired.

Reconnaissance findings currently include:

- source IP;
- destination IP;
- distinct destination ports;
- packet count;
- observation window;
- rule identifier;
- severity;
- finding title.

## Cryptographic Evidence Rules

### SHA-256

SHA-256 is used as a deterministic digest of evidence bytes.

### HMAC-SHA256

HMAC-SHA256 demonstrates integrity/authentication with a shared secret.

The repository's tests use a clearly labeled test-only secret. Demonstration secrets must never be committed as production credentials.

### Manifest Verification

The evidence manifest records:

- schema version;
- evidence SHA-256;
- evidence HMAC-SHA256;
- finding count;
- serialized findings.

Verification checks the artifact against both the recorded digest and HMAC.

## Reporting Rules

JSON is the machine-readable finding representation.

HTML is the analyst-readable report representation.

Reports must not claim that a finding proves compromise, attribution, intent, or universal detection coverage.

## Testing Rules

The test suite should cover:

- positive TCP detection;
- below-threshold TCP non-detection;
- TCP SYN/ACK non-detection;
- positive UDP detection;
- protocol normalization;
- TCP flag normalization;
- IP normalization;
- TCP/UDP transport-port extraction;
- TShark field parsing with embedded commas;
- JSON parsing;
- SHA-256/HMAC verification;
- evidence-manifest tampering;
- HTML report generation.

## CI Rules

The main branch is considered healthy when the latest CI workflow succeeds.

GitHub Actions validates:

- Ubuntu;
- Windows;
- Python 3.11;
- Python 3.12;
- Python 3.13;
- Python 3.14;
- editable package installation;
- the complete pytest suite;
- deterministic CLI execution;
- HTML report creation.

A CI failure must be understood and fixed at the underlying implementation, test, packaging, or configuration layer.

## Dependency Rules

The core application has no runtime third-party Python dependencies.

pytest is a development/test dependency.

TShark is an external tool used only by the PCAP adapter for real-capture analysis.

## External Tool Roles

| Tool | Role |
|---|---|
| VMware Workstation | Controlled virtualization |
| Kali Linux | Authorized test host |
| Metasploitable | Controlled vulnerable target |
| Nmap | Generates authorized reconnaissance traffic |
| Wireshark | Packet capture and visual inspection |
| TShark | Packet-field extraction for NetDefender |
| GitHub Actions | Automated software validation |

NetDefender remains the primary software artifact.

## Lab Safety Rules

All security testing must remain inside the controlled lab.

Never target public IP addresses, university networks, third-party systems, neighbors' devices, unrelated host devices, or systems without explicit authorization.

Metasploitable must remain isolated because it is intentionally vulnerable.

## Current MVP Contract

The current supported MVP consists of the two documented reconnaissance rules, JSON/CSV parsing, real PCAP/PCAPNG analysis through TShark, cryptographic evidence helpers, JSON/HTML reporting, automated tests, and CI validation.

The MVP is intended for controlled course demonstration rather than production deployment.
