# NetDefender
**Network Security Monitoring & Cryptographic Evidence Lab**

## Overview

NetDefender is a controlled network-security lab and software project for **ISCI 6101: Network Security Engineering & Cryptography**. The project combines a small Kali/Metasploitable virtual lab with a purpose-built security analysis application.

The goal is to make network-security concepts observable through code instead of building a large collection of unrelated enterprise products.

NetDefender is intentionally **not a monolithic enterprise appliance**. The virtual machines generate controlled traffic, while NetDefender performs the coding-heavy analysis, detection, evidence integrity, and reporting work.

## Core Flow

```text
Build Isolated Lab
       ↓
Controlled Reconnaissance
       ↓
Capture Network Traffic
       ↓
NetDefender Analysis
       ↓
Detect Suspicious Activity
       ↓
Cryptographically Protect Evidence
       ↓
Review Detection Report
       ↓
Automated CI Validation
```

## Problem

Network reconnaissance can generate observable traffic before an attack reaches an application or host. A security analyst needs to turn that low-level network activity into understandable evidence while preserving confidence that the evidence was not modified.

NetDefender explores that workflow by detecting selected reconnaissance patterns in controlled network data and using cryptographic mechanisms to verify evidence integrity.

## Objectives

- Build an isolated Kali Linux → Metasploitable security-testing lab.
- Generate authorized reconnaissance traffic with Nmap.
- Capture and inspect that traffic with Wireshark/tshark.
- Build a Python-based network event parser and detection engine.
- Detect selected port-scanning/reconnaissance behavior from structured traffic data.
- Produce readable security findings and evidence.
- Use SHA-256 and HMAC to demonstrate evidence integrity and authenticity concepts.
- Add automated unit/integration tests.
- Validate the project automatically with GitHub Actions.
- Keep the project focused enough to be reproducible while still demonstrating real network-security engineering.

## MVP Scope

### Lab

- VMware Workstation
- Kali Linux — controlled testing host
- Metasploitable — controlled target
- Isolated virtual networking
- Nmap — reconnaissance generation
- Wireshark/tshark — packet capture and inspection

### NetDefender Software

- **Python** security-analysis engine
  - network-event models
  - packet/event parsing
  - reconnaissance detector
  - finding/report generation
  - cryptographic evidence utilities
- **Optional TypeScript web interface** in a later phase if it improves the final demonstration without adding unnecessary infrastructure.
- **pytest** automated tests
- **GitHub Actions** CI

The project may use more than one language when it provides a clear engineering benefit. Languages are not being added merely to increase the technology count.

## Architecture

```text
              CONTROLLED LAB

       +-------------------+
       |     Kali Linux    |
       |  Nmap / Testing   |
       +---------+---------+
                 |
                 | controlled traffic
                 v
       +-------------------+
       |   Metasploitable  |
       |      Target       |
       +---------+---------+
                 |
                 | observed packets
                 v
       +-------------------+
       | Wireshark / tshark|
       | Capture + Evidence|
       +---------+---------+
                 |
                 | pcap / structured events
                 v
       +-----------------------------+
       |        NetDefender          |
       |-----------------------------|
       | Parser → Detector → Report  |
       |             ↓               |
       |       Crypto Integrity      |
       +-------------+---------------+
                     |
                     v
              Security Findings
                     |
                     v
              GitHub Actions
```

The external tools are the **controlled lab environment**. The primary engineering deliverable is the NetDefender software and its tests/evidence.

## Technology Choices

| Area | Technology | Reason |
|---|---|---|
| Lab virtualization | VMware Workstation | Existing isolated VM environment |
| Test host | Kali Linux | Controlled security testing |
| Target | Metasploitable | Intentionally vulnerable lab target |
| Reconnaissance | Nmap | Repeatable network discovery/scanning |
| Packet analysis | Wireshark / tshark | Observable packet-level evidence |
| Core application | Python | Strong networking/data-processing ecosystem and easy testing |
| Optional UI | TypeScript | Can provide a polished browser-facing report without changing the core engine |
| Testing | pytest | Repeatable automated validation |
| Cryptography | Python standard library / approved crypto libraries as needed | SHA-256/HMAC evidence integrity demonstrations |
| CI | GitHub Actions | Automated project verification |
| Version control | Git / GitHub | Source, evidence, documentation, and CI history |

## Phase Plan

| Phase | Focus | Status |
|---|---|---|
| 1 | Isolated lab + software foundation | **In progress** |
| 2 | Reconnaissance data collection | Planned |
| 3 | Traffic parsing and event normalization | Planned |
| 4 | Detection engine and findings | Planned |
| 5 | Cryptographic evidence integrity | Planned |
| 6 | Security report / optional TypeScript UI | Planned |
| 7 | Testing, CI, and validation | Planned |
| 8 | Final integrated scenarios and evidence | Planned |
| 9 | Final report and presentation | Planned |

## Project Structure

```text
NetDefender/
├── netdefender/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── detectors.py
│   ├── crypto.py
│   └── models.py
├── tests/
├── data/
│   └── samples/
├── docs/
│   ├── architecture.md
│   ├── setup.md
│   └── evidence.md
├── figures/
├── .github/
│   └── workflows/
│       └── tests.yml
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Security Concepts Demonstrated

- Network reconnaissance and attack-surface discovery
- TCP/UDP behavior
- Packet-level traffic analysis
- Detection logic and security events
- Network-security monitoring
- Hashing with SHA-256
- HMAC and message authenticity
- Evidence integrity
- Repeatable security testing
- Defense-in-depth concepts
- Automated security validation through CI

## Final Demonstration

The intended final scenario is:

1. Kali performs an authorized Nmap scan against Metasploitable.
2. Traffic is captured in the isolated lab.
3. NetDefender parses the captured/structured traffic.
4. The detector identifies the reconnaissance pattern.
5. NetDefender creates a finding containing evidence and metadata.
6. A SHA-256 digest and HMAC are generated for the evidence.
7. The evidence is deliberately checked for integrity.
8. NetDefender produces a readable security report.
9. GitHub Actions runs the automated tests and verifies the project.

No result will be presented as real-world attack detection capability beyond the controlled scenarios actually tested.

## Security Scope

All security testing must remain inside the NetDefender virtual lab. Kali/Nmap traffic must target only the user's Metasploitable VM or other explicitly authorized NetDefender lab systems.

Do not scan university networks, public IP addresses, third-party systems, or unrelated host devices.

## Limitations

- The MVP focuses on selected reconnaissance patterns rather than all network attacks.
- Detection quality depends on the packet/event data supplied to the analyzer.
- The virtual lab does not represent a production enterprise network.
- Evidence integrity mechanisms demonstrate cryptographic concepts; they do not by themselves establish legal chain of custody.
- Metasploitable is intentionally vulnerable and should remain isolated.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup](docs/setup.md)
- [Evidence](docs/evidence.md)
