# NetDefender

**Controlled Network Reconnaissance Detection & Cryptographic Evidence Lab**

## Overview

NetDefender is a controlled network-security software project for **ISCI 6101: Network Security Engineering & Cryptography**. It analyzes normalized network events and real PCAP/PCAPNG captures from an isolated VMware lab, detects selected reconnaissance patterns, preserves explainable evidence, and produces machine-readable JSON and dependency-free HTML reports.

The controlled lab uses Kali Linux, Metasploitable, Nmap, and Wireshark/TShark to generate and capture authorized traffic. NetDefender is the primary software artifact that parses that evidence, normalizes packet fields, applies deterministic detection rules, and presents the results.

## Problem

Network reconnaissance can produce recognizable traffic patterns, but packet captures are difficult to interpret consistently without a defined analysis process. NetDefender turns selected reconnaissance behaviors into explicit, testable rules so that controlled TCP and UDP scans can be analyzed from the same captured evidence.

## Objectives

- Parse normalized network events from JSON and CSV input.
- Analyze PCAP/PCAPNG captures through TShark.
- Normalize protocol, transport-port, IP, timestamp, TCP-flag, and packet-length fields.
- Detect controlled TCP SYN reconnaissance.
- Detect controlled UDP reconnaissance.
- Produce explainable findings with source, target, ports, packet count, and observation window.
- Demonstrate SHA-256 and HMAC-SHA256 evidence integrity concepts.
- Detect controlled evidence tampering through manifest verification.
- Generate concise JSON and HTML reports.
- Validate the software with automated tests and GitHub Actions.

## MVP Scope

- Python 3.11+ command-line application.
- JSON and CSV network-event parsing.
- PCAP/PCAPNG analysis through the optional TShark adapter.
- `NET-RECON-001` TCP SYN reconnaissance detection.
- `NET-RECON-002` UDP reconnaissance detection.
- Deterministic, explainable findings.
- SHA-256 and HMAC-SHA256 evidence helpers.
- Tamper-detecting evidence manifests.
- Dependency-free HTML security reports.
- Linux and Windows setup scripts.
- Automated pytest coverage and GitHub Actions validation.
- Controlled Kali → Metasploitable network evidence for TCP and UDP demonstrations.

## Architecture / Workflow

```text
Controlled VMware Lab
Kali Linux
  │
  └── Nmap generates authorized TCP/UDP traffic
          │
          ▼
Metasploitable
          │
          ▼
Wireshark / TShark
          │
          └── PCAP / PCAPNG
                  │
                  ▼
            NetDefender
                  │
          TShark field extraction
                  │
                  ▼
          Parser / Normalizer
                  │
                  ▼
          NetworkEvent objects
                  │
                  ▼
          Detection Engine
             │          │
             ▼          ▼
        TCP SYN       UDP
        rule 001     rule 002
             │          │
             └────┬─────┘
                  ▼
             Findings
                  │
          ┌───────┴────────┐
          ▼                ▼
       JSON output      HTML report
```

Cryptographic evidence helpers are available as a separate evidence workflow:

```text
Evidence artifact
      ↓
SHA-256 digest
      ↓
HMAC-SHA256 tag
      ↓
Integrity manifest
      ↓
Verify original artifact
      ↓
Modify artifact
      ↓
Verification fails
```

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| Application | Python standard library |
| Testing | pytest |
| Packet analysis | TShark |
| Packet capture / inspection | Wireshark |
| Controlled test host | Kali Linux |
| Controlled target | Metasploitable |
| Traffic generation | Nmap |
| Virtualization | VMware Workstation |
| Integrity | SHA-256 + HMAC-SHA256 |
| Reporting | Dependency-free HTML + JSON |
| Version Control | Git / GitHub |
| CI | GitHub Actions |

## Project Structure

```text
NetDefender/
├── netdefender/
│   ├── analyzer.py
│   ├── capture.py
│   ├── cli.py
│   ├── crypto.py
│   ├── detectors.py
│   ├── evidence.py
│   ├── models.py
│   ├── parser.py
│   └── report.py
├── tests/
│   └── test_netdefender.py
├── data/
│   └── samples/
│       └── syn-scan.json
├── docs/
│   ├── architecture.md
│   ├── evidence.md
│   ├── pcap.md
│   ├── rules.md
│   └── setup.md
├── scripts/
│   ├── setup.sh
│   └── setup.ps1
├── topology/
│   └── ip-plan.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Security Concepts

- Network reconnaissance and port scanning
- TCP SYN scanning
- UDP reconnaissance
- Packet capture and network-event normalization
- Deterministic detection rules
- Explainable security findings
- SHA-256 evidence hashing
- HMAC-SHA256 integrity/authenticity concepts
- Evidence tampering detection
- Controlled security testing
- Security evidence and reporting

## Expected Demonstration

Run controlled reconnaissance traffic from Kali against the isolated Metasploitable VM, capture the traffic with Wireshark, and analyze the resulting PCAP/PCAPNG with NetDefender.

For the TCP scenario, an authorized Nmap SYN scan produces traffic across many TCP destination ports. NetDefender extracts the packet fields through TShark and detects the documented `NET-RECON-001` threshold.

For the UDP scenario, an authorized Nmap UDP scan produces probes across multiple UDP destination ports. NetDefender detects the documented `NET-RECON-002` threshold and reports the observed destination ports, packet count, and time window.

For the control scenario, below-threshold TCP traffic is analyzed and produces no finding. This demonstrates that the detector does not fire simply because TCP traffic exists.

The HTML reports present the same findings in a concise analyst-readable format. The cryptographic evidence helpers separately demonstrate how an evidence artifact can be hashed, authenticated with HMAC-SHA256, and checked for later modification.

## Security Scope and Limitations

NetDefender is a local course-project security laboratory, not a production intrusion-detection system. Its detection engine intentionally covers only two reconnaissance patterns with fixed, documented thresholds.

A finding means that the observed events matched a defined NetDefender rule. It does not by itself prove malicious intent, compromise, attribution, or that the traffic represents an attack in every environment.

Real PCAP analysis requires TShark to be installed. The core JSON/CSV application does not require TShark.

The VMware environment must remain isolated because Metasploitable is intentionally vulnerable. Nmap testing must target only the authorized lab systems.

SHA-256 and HMAC-SHA256 provide integrity/authentication mechanisms for the controlled evidence demonstration, but they do not by themselves establish a legal chain of custody.

## Final MVP Status

The NetDefender MVP is **functionally complete and ready for course submission**. The implemented parser, PCAP/TShark adapter, TCP and UDP detection rules, cryptographic evidence helpers, reporting, automated tests, setup automation, and CI are documented and synchronized with the implementation.

The real controlled lab has been validated with TCP and UDP Nmap traffic. The current automated test suite passes **17/17 tests**, and the TCP positive, TCP control, and UDP HTML reports have been generated from the corresponding evidence.

Final work is limited to organizing the validated evidence and preparing the course presentation/submission materials.

## Out of Scope

- Internet-wide or arbitrary network scanning
- Production intrusion-detection deployment
- Full penetration-testing automation
- Enterprise SIEM functionality
- Large vulnerability databases
- Malware analysis
- Universal attack detection
- Generic security scoring
- Uncontrolled scanning of third-party systems

## Future Enhancements

- Additional deterministic reconnaissance rules.
- More protocol-aware traffic analysis.
- Expanded PCAP evidence extraction.
- Additional evidence-manifest workflows.
- Optional analyst-facing interface if a concrete need is identified.
- Expanded automated test fixtures for additional traffic patterns.

## Verification

From the repository root, activate the project virtual environment and run:

```bash
python -m pytest
```

The current suite should complete with:

```text
17 passed
```

To run the deterministic sample and generate an HTML report:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

For a real PCAP/PCAPNG capture, with TShark installed:

```bash
python -m netdefender.cli /path/to/capture.pcapng --html report.html
```

The GitHub Actions workflow validates package installation, the full test suite, CLI execution, and HTML report generation across Ubuntu and Windows with Python 3.11–3.14.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup](docs/setup.md)
- [PCAP Analysis](docs/pcap.md)
- [Detection Rules](docs/rules.md)
- [Evidence](docs/evidence.md)
- [Lab IP Plan](topology/ip-plan.md)
