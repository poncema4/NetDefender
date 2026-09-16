# NetDefender
**Network Security Monitoring & Cryptographic Evidence Lab**

## Overview

NetDefender is a controlled network-security lab and software project for **ISCI 6101: Network Security Engineering & Cryptography**. It combines a small Kali/Metasploitable virtual lab with a purpose-built security-analysis application.

The goal is to make network-security and cryptography concepts observable through code without turning the project into a collection of unrelated enterprise products.

NetDefender is **not a monolithic appliance**. The virtual machines generate controlled traffic; NetDefender performs the primary coding, parsing, detection, cryptographic evidence, and reporting work.

## Core Flow

```text
Kali / Nmap
    ↓
Metasploitable
    ↓
Wireshark / tshark
    ↓
Network events
    ↓
NetDefender Parser
    ↓
Detection Engine
    ↓
Findings + Evidence
    ↓
SHA-256 / HMAC
    ↓
JSON + HTML Report
    ↓
GitHub Actions
```

## Problem

Network reconnaissance produces observable traffic, but raw packets are difficult to interpret as a security finding. NetDefender turns selected network observations into explainable detections and then demonstrates how cryptographic integrity mechanisms can protect the resulting evidence.

## Objectives

- Build a controlled Kali Linux → Metasploitable lab.
- Generate authorized TCP and UDP reconnaissance traffic with Nmap.
- Capture and inspect traffic with Wireshark/tshark.
- Parse structured network observations into a stable data model.
- Detect selected reconnaissance patterns with deterministic rules.
- Produce explainable security findings.
- Generate SHA-256 and HMAC-SHA256 evidence metadata.
- Verify evidence integrity after controlled modification.
- Generate JSON and dependency-free HTML reports.
- Maintain automated tests and GitHub Actions CI.

## MVP Scope

### Controlled Lab

- VMware Workstation
- Kali Linux — authorized testing host
- Metasploitable — authorized vulnerable target
- Isolated virtual networking
- Nmap — reconnaissance traffic generation
- Wireshark/tshark — packet capture and inspection

### NetDefender Software

- Python network-event models
- JSON/CSV parser
- TCP SYN reconnaissance detector
- UDP reconnaissance detector
- Finding/report generation
- SHA-256 evidence hashing
- HMAC-SHA256 integrity/authenticity demonstration
- HTML security report generator
- pytest automated tests
- GitHub Actions CI

A TypeScript interface remains an optional future enhancement. It is not being added merely to increase the technology count.

## Architecture

```text
┌──────────────────── CONTROLLED LAB ────────────────────┐
│                                                        │
│   Kali Linux ── Nmap ──> Metasploitable               │
│       │                         │                      │
│       └────── Wireshark/tshark capture ───────────────┘
└───────────────────────────┬────────────────────────────┘
                            │ structured events
                            v
┌────────────────────────────────────────────────────────┐
│                    NETDEFENDER                         │
│                                                        │
│ Parser → Normalizer → Detection Engine → Findings      │
│                                      ↓                 │
│                              SHA-256 + HMAC             │
│                                      ↓                 │
│                              JSON / HTML                │
└───────────────────────────┬────────────────────────────┘
                            v
                    GitHub Actions CI
```

## Project Structure

```text
NetDefender/
├── netdefender/
│   ├── __init__.py
│   ├── analyzer.py
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
│   ├── setup.md
│   └── evidence.md
├── topology/
│   └── ip-plan.md
├── evidence/
├── figures/
├── .github/workflows/tests.yml
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Technology Choices

| Area | Technology | Purpose |
|---|---|---|
| Core application | Python 3.11+ | Parsing, detection, crypto, reporting |
| Testing | pytest | Automated validation |
| Lab | VMware Workstation | Isolated virtual machines |
| Test host | Kali Linux | Controlled security testing |
| Target | Metasploitable | Controlled vulnerable target |
| Reconnaissance | Nmap | Repeatable TCP/UDP scans |
| Traffic evidence | Wireshark / tshark | Packet observation and export |
| Integrity | SHA-256 + HMAC-SHA256 | Evidence integrity/authenticity concepts |
| CI | GitHub Actions | Repeatable automated checks |

## Phase Plan

The phases are intentionally **coding-first**. This lets the software be developed and tested while away from the laptop. When the laptop is available, the remaining work is primarily connecting the already-built software to real lab traffic and collecting evidence.

| Phase | Focus | Can be done away from laptop? | Status |
|---|---|---:|---|
| 1 | Architecture + data model | Yes | **Complete** |
| 2 | Parser + validation | Yes | **Implemented** |
| 3 | TCP/UDP detection engine | Yes | **Implemented** |
| 4 | Cryptographic evidence | Yes | **Implemented** |
| 5 | Security reporting | Yes | **Implemented** |
| 6 | Automated testing + CI | Yes | **Implemented / expanding** |
| 7 | VMware lab configuration | No | Pending |
| 8 | Real Nmap + Wireshark collection | No | Pending |
| 9 | End-to-end validation + evidence | Partly | Pending |
| 10 | Final report + presentation | Yes | Pending |

## Current Software Capabilities

The code can already accept normalized JSON or CSV network events, run the reconnaissance detection engine, emit structured findings, and generate an HTML report. The repository also contains a controlled synthetic scan sample for deterministic development/testing.

Example command once the repository is cloned:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html report.html
```

## Security Concepts Demonstrated

- Network reconnaissance and attack-surface discovery
- TCP SYN scanning behavior
- UDP scanning behavior
- Packet/event normalization
- Explainable network detection
- SHA-256 hashing
- HMAC-SHA256
- Evidence integrity verification
- Repeatable security testing
- Automated CI validation

## Final Demonstration

The intended final scenario is:

1. Kali performs an authorized Nmap scan against the user's Metasploitable VM.
2. Wireshark/tshark captures the resulting traffic.
3. Relevant traffic is exported into NetDefender's event format.
4. NetDefender parses and normalizes the events.
5. Detection rules identify the reconnaissance pattern.
6. A security finding is generated with supporting evidence.
7. SHA-256 and HMAC metadata are generated.
8. The evidence is deliberately modified and verification demonstrates the integrity check failing.
9. A readable JSON/HTML report is produced.
10. GitHub Actions validates the code and tests.

No result will be presented as general-purpose real-world IDS capability; conclusions will be limited to the controlled scenarios actually tested.

## Security Scope

All security testing must remain inside the NetDefender virtual lab. Kali/Nmap traffic must target only the user's Metasploitable VM or another explicitly authorized NetDefender lab system.

Do not scan university networks, public IP addresses, third-party systems, or unrelated host devices.

## Limitations

- Detection focuses on selected reconnaissance patterns rather than all attacks.
- Detection quality depends on the event fields supplied to the analyzer.
- The virtual lab is not a production enterprise network.
- SHA-256/HMAC demonstrations do not by themselves establish legal chain of custody.
- Metasploitable is intentionally vulnerable and must remain isolated.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup](docs/setup.md)
- [Evidence](docs/evidence.md)
- [IP Plan](topology/ip-plan.md)
