# NetDefender
**Network Security Monitoring & Cryptographic Evidence Lab**

## Overview

NetDefender is a controlled network-security lab and software project for **ISCI 6101: Network Security Engineering & Cryptography**. It combines a small Kali/Metasploitable virtual lab with a purpose-built security-analysis application.

The goal is to make network-security and cryptography concepts observable through code without turning the project into a collection of unrelated enterprise products.

The virtual machines generate controlled traffic; NetDefender performs the primary coding, parsing, detection, cryptographic evidence, and reporting work.

## Core Flow

```text
Kali / Nmap
    ↓
Metasploitable
    ↓
Wireshark / tshark
    ↓
PCAP / normalized events
    ↓
Parser / normalizer
    ↓
Detection engine
    ↓
Findings + evidence
    ↓
SHA-256 / HMAC
    ↓
JSON + HTML report
    ↓
GitHub Actions CI
```

## Current Software Scope

- Python network-event models
- JSON/CSV parsing and normalization
- Optional PCAP/PCAPNG analysis through tshark
- `NET-RECON-001` TCP SYN reconnaissance detection
- `NET-RECON-002` UDP reconnaissance detection
- Explainable finding generation
- SHA-256 evidence hashing
- HMAC-SHA256 integrity/authenticity demonstration
- Tamper-detecting evidence manifests
- Dependency-free HTML reports
- pytest automated tests
- Linux setup script
- Windows PowerShell setup script
- GitHub Actions matrix across Ubuntu/Windows and Python 3.11–3.14

The complete detection/project contract is in [`docs/rules.md`](docs/rules.md).

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
├── data/samples/
├── docs/
│   ├── architecture.md
│   ├── evidence.md
│   ├── rules.md
│   └── setup.md
├── scripts/
│   ├── setup.sh
│   └── setup.ps1
├── topology/
├── .github/workflows/tests.yml
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Local Setup

### Linux

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

Both scripts create `.venv`, install the package/test dependency, run the complete test suite, run the deterministic sample, generate `local-report.html`, and report whether optional tshark is available.

For the detailed setup, troubleshooting, PCAP workflow, and VMware instructions, see [`docs/setup.md`](docs/setup.md).

## Synthetic Smoke Test

The core application can be tested without VMware:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html report.html
```

The synthetic sample is version-controlled specifically so software behavior can be tested deterministically before real lab traffic exists.

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

A TypeScript interface remains optional. It will only be added if it solves a real analyst-facing problem rather than increasing the technology count.

## Phase Plan

The project is intentionally **coding-first** so software that can be built away from the laptop is completed before the physical lab work.

| Phase | Focus | Location | Status |
|---|---|---|---|
| 1 | Architecture + data model | Anywhere | **Complete** |
| 2 | Parser + validation | Anywhere | **Implemented** |
| 3 | Detection engine | Anywhere | **Implemented** |
| 4 | Cryptographic evidence | Anywhere | **Implemented** |
| 5 | Reporting | Anywhere | **Implemented** |
| 6 | Automated testing + CI + local setup automation | Anywhere | **Complete / verified** |
| 7 | VMware lab configuration | Laptop | **Next** |
| 8 | Real Nmap + Wireshark collection | Laptop | Pending |
| 9 | End-to-end validation + evidence | Partly | Pending |
| 10 | Final report + presentation | Anywhere | Pending |

**Phase 1 is complete.** The coding-first milestone through Phase 6 is now also complete because the latest commit has been verified by the full CI matrix. Phase 7 is the next phase: configuring the actual VMware lab.

## CI Definition of Done

The CI pipeline intentionally goes beyond a single `pytest` call. It validates:

- Ubuntu;
- Windows;
- Python 3.11;
- Python 3.12;
- Python 3.13;
- Python 3.14;
- editable package installation;
- the complete pytest suite;
- CLI execution;
- generated HTML report existence.

The latest verified run passed all eight matrix jobs. This is a software/CI validation result, not a claim that the VMware lab has already been tested.

GitHub's current `setup-python` documentation recommends explicitly selecting Python versions and supports dependency caching; NetDefender follows that model in CI.

## Final Demonstration

The intended final scenario is:

1. Kali performs an authorized Nmap scan against the user's Metasploitable VM.
2. Wireshark/tshark captures the resulting traffic.
3. Relevant traffic is analyzed as PCAP or exported into NetDefender's normalized event format.
4. NetDefender parses and normalizes the evidence.
5. Detection rules identify the controlled reconnaissance pattern.
6. A security finding is generated with supporting evidence.
7. SHA-256 and HMAC metadata are generated.
8. Evidence is deliberately modified and verification demonstrates tamper detection.
9. A readable JSON/HTML report is produced.
10. CI validates the software.

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

- [`docs/setup.md`](docs/setup.md) — complete Linux/Windows setup, troubleshooting, PCAP, and VMware workflow
- [`docs/rules.md`](docs/rules.md) — detection, testing, CI, safety, evidence, and project rules
- [`docs/architecture.md`](docs/architecture.md) — architecture and phase boundaries
- [`docs/evidence.md`](docs/evidence.md) — evidence workflow
- [`topology/ip-plan.md`](topology/ip-plan.md) — lab addressing notes
