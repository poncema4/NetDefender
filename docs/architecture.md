# NetDefender Architecture

## Purpose

NetDefender is a controlled network-security analysis application for ISCI 6101: Network Security Engineering & Cryptography. The software is intentionally focused: the VMware lab generates controlled traffic, while NetDefender performs the parsing, normalization, detection, evidence, and reporting work.

## High-Level Architecture

```text
┌──────────────────── CONTROLLED LAB ────────────────────┐
│                                                       │
│   Kali Linux ── Nmap ──> Metasploitable              │
│        │                         │                     │
│        └──── Wireshark / TShark capture ──────────────┘
└───────────────────────────┬───────────────────────────┘
                            │ PCAP / PCAPNG
                            ▼
┌────────────────────────────────────────────────────────┐
│                    NETDEFENDER                         │
│                                                        │
│ PCAP → TShark extraction → Parser / Normalizer         │
│                              │                         │
│                              ▼                         │
│                       NetworkEvent                     │
│                              │                         │
│                              ▼                         │
│                      Detection Engine                  │
│                         │          │                   │
│                         ▼          ▼                   │
│                    TCP rule      UDP rule              │
│                         │          │                   │
│                         └────┬─────┘                   │
│                              ▼                         │
│                         Findings                       │
│                              │                         │
│                    ┌─────────┴─────────┐               │
│                    ▼                   ▼               │
│                 JSON output        HTML report         │
└────────────────────────────────────────────────────────┘
```

Cryptographic evidence is implemented as a reusable evidence layer:

```text
Evidence bytes
     ↓
SHA-256 + HMAC-SHA256
     ↓
Integrity manifest
     ↓
Verification
     ↓
Original artifact = valid
Modified artifact = rejected
```

## Core Components

### Network Event Model

`NetworkEvent` provides a stable representation of one observed packet/event: timestamp, source and destination IP addresses, protocol, source and destination ports, TCP flags, and packet length.

`Finding` represents an explainable detection result with a rule identifier, title, severity, source, destination, and evidence dictionary.

### Input Parser

`parser.py` accepts JSON arrays and CSV event data. It normalizes timestamps, numeric fields, protocol text, and TCP flags supplied through normalized input.

### PCAP / TShark Adapter

`capture.py` invokes TShark for PCAP/PCAPNG input and extracts:

- packet timestamp;
- source IP;
- destination IP;
- numeric IP protocol;
- TCP source/destination ports;
- UDP source/destination ports;
- TCP flags;
- packet length.

The adapter converts those fields into the same `NetworkEvent` model used by JSON/CSV input. It also normalizes TShark protocol values, TCP flag bitmasks, transport ports, and comma-separated IP fields.

### Detection Engine

The detection engine currently contains two deterministic rules:

- `NET-RECON-001` — TCP SYN reconnaissance: at least 10 distinct TCP destination ports from one source to one target within 10 seconds, with SYN and without ACK.
- `NET-RECON-002` — UDP reconnaissance: at least 8 distinct UDP destination ports from one source to one target within 10 seconds.

The rules produce explainable evidence including destination ports, packet count, and observation window.

### Cryptographic Evidence

`crypto.py` provides SHA-256 and HMAC-SHA256 helpers. `evidence.py` builds an integrity manifest containing the evidence digest, HMAC, finding count, and findings, and verifies both digest and HMAC.

These functions are available for the controlled evidence workflow; the basic CLI report path does not automatically create a cryptographic manifest.

### Reporting

`report.py` generates a dependency-free HTML report from findings. The CLI prints findings as JSON and can optionally write the same findings to an HTML report.

### CLI

`cli.py` accepts JSON, CSV, PCAP, and PCAPNG evidence files. Input format is inferred from the file extension unless explicitly supplied. The CLI runs the analyzer and prints stable JSON; `--html` writes an analyst-readable report.

## End-to-End Workflow

```text
1. Generate authorized traffic in the isolated lab.
2. Capture the traffic with Wireshark/TShark.
3. Save the PCAP/PCAPNG evidence.
4. Give the capture to NetDefender.
5. TShark extracts the required packet fields.
6. NetDefender normalizes the fields into NetworkEvent objects.
7. Detection rules evaluate the normalized events.
8. Matching conditions become Finding objects.
9. Findings are printed as JSON and can be written as HTML.
10. Evidence integrity can be demonstrated separately with SHA-256/HMAC-SHA256.
```

## Design Decisions

### Why Python?

Python keeps parsing, detection, cryptography, reporting, and testing in one cohesive codebase while minimizing installation overhead on the lab machine.

### Why use TShark instead of a Python PCAP dependency?

The project uses TShark as a bounded adapter for real packet captures. This keeps the core application dependency-free while still allowing NetDefender to process real PCAP/PCAPNG evidence.

### Why not add many security products?

The project is designed around a small controlled lab and a purpose-built application. Adding multiple enterprise products would shift the project toward infrastructure configuration instead of software engineering.

### Why no frontend framework?

The current dependency-free HTML report provides sufficient analyst-readable output for the MVP without introducing a separate frontend application.

## CI Design

GitHub Actions tests the actual package installation across Ubuntu and Windows using Python 3.11, 3.12, 3.13, and 3.14. It runs the complete pytest suite, the CLI against the deterministic sample, and an HTML report existence check.

## Security Boundary

All Nmap/security testing must remain inside the controlled VMware lab and target only the authorized Metasploitable VM or another explicitly authorized lab system.

No conclusion from NetDefender should be presented as broader than the controlled traffic and documented rules actually tested.
