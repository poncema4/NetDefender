# NetDefender Architecture

## 1. Purpose

NetDefender is a controlled network-security laboratory backed by a purpose-built analysis application for ISCI 6101: Network Security Engineering & Cryptography.

The project deliberately keeps external infrastructure small. The user's VMware lab supplies controlled traffic; NetDefender supplies the primary software engineering, detection, cryptographic evidence, and reporting work.

## 2. High-Level Architecture

```text
┌──────────────────── CONTROLLED LAB ────────────────────┐
│                                                        │
│   Kali Linux ── Nmap ──> Metasploitable               │
│       │                         │                      │
│       └────── Wireshark/tshark capture ───────────────┘
└───────────────────────────┬────────────────────────────┘
                            │ pcap / structured events
                            v
┌────────────────────────────────────────────────────────┐
│                    NETDEFENDER                         │
│                                                        │
│ Input → Parser → Normalizer → Detection Engine         │
│                              │                         │
│                              v                         │
│                    Findings + Evidence                 │
│                              │                         │
│                              v                         │
│                     SHA-256 + HMAC                     │
│                              │                         │
│                              v                         │
│                     HTML / JSON Report                 │
└───────────────────────────┬────────────────────────────┘
                            v
                    GitHub Actions CI
```

## 3. Core Components

### 3.1 Network Event Model

`NetworkEvent` provides a stable representation of observed traffic: timestamp, source/destination addresses, protocol, ports, TCP flags, and packet length. Detection rules do not depend on the original capture format.

### 3.2 Input Parser

The parser accepts JSON and CSV event data and normalizes timestamps and numeric fields. The optional PCAP adapter invokes tshark and converts selected packet fields into the same event model.

### 3.3 Detection Engine

The supported reconnaissance rules are:

- `NET-RECON-001`: burst of TCP SYN probes to many destination ports.
- `NET-RECON-002`: burst of UDP probes to many destination ports.

Rules are intentionally deterministic and explainable. A finding records the rule, source, target, severity, port evidence, packet count, and observation window.

The complete rule contract is documented in `docs/rules.md`.

### 3.4 Cryptographic Evidence

SHA-256 creates a deterministic digest of an evidence artifact. HMAC-SHA256 demonstrates integrity/authenticity when a shared secret is available. Verification uses constant-time comparison for the HMAC check.

The crypto layer is connected to the detection workflow: NetDefender produces evidence, then creates and verifies cryptographic metadata for that evidence.

### 3.5 Reporting

The application generates structured findings and a dependency-free HTML report. A TypeScript browser interface remains a possible later enhancement, but it will only be added if it solves a real analyst-facing problem.

### 3.6 Local Setup Automation

The repository provides:

- `scripts/setup.sh` for Linux-like shells;
- `scripts/setup.ps1` for Windows PowerShell;
- `docs/setup.md` as the detailed setup and troubleshooting guide.

The setup scripts create the virtual environment, install the project/test dependency, run the complete test suite, run the deterministic CLI sample, and check optional tshark availability.

## 4. Current Software Flow

```text
JSON/CSV events OR PCAP/PCAPNG
              ↓
      Parser / tshark adapter
              ↓
       NetworkEvent objects
              ↓
      Reconnaissance rules
              ↓
         Finding objects
              ↓
      JSON + HTML report
              ↓
   SHA-256 / HMAC evidence
              ↓
       Integrity verification
```

## 5. Phase Organization

The phases are intentionally ordered so all coding that can be completed away from the laptop happens first. The physical lab work comes after the software is ready.

| Phase | Focus | Work location | Status |
|---|---|---|---|
| 1 | Software architecture + data model | Anywhere | **Complete** |
| 2 | Parser + validation | Anywhere | **Implemented** |
| 3 | Detection engine | Anywhere | **Implemented** |
| 4 | Cryptographic evidence | Anywhere | **Implemented** |
| 5 | Reporting / analyst output | Anywhere | **Implemented** |
| 6 | Automated testing + GitHub Actions + local setup automation | Anywhere | **In verification** |
| 7 | VMware lab setup | Laptop | Pending |
| 8 | Real Nmap + Wireshark integration | Laptop | Pending |
| 9 | End-to-end validation + evidence | Laptop | Pending |
| 10 | Final report + presentation | Anywhere | Pending |

### Phase 6 definition of done

Phase 6 is not considered complete merely because a workflow file exists. The latest commit must have a successful CI run across the supported matrix, and the failure history must be understood and corrected at the underlying implementation/test/configuration layer.

Once Phase 6 is verified green, the coding-first milestone is complete and the project moves to Phase 7.

## 6. Design Decisions

### Why Python?

Python keeps parsing, detection, cryptography, reporting, and testing in one cohesive codebase. It also minimizes installation burden on the lab machine.

### Why not add many enterprise products?

pfSense, Snort, OpenVPN, and similar systems can demonstrate useful concepts, but using all of them would turn the project into an infrastructure-configuration project. NetDefender instead uses a small controlled lab and puts the engineering depth into the software itself.

### Why not add another language immediately?

A second language is useful only when it solves a real project problem. The current dependency-free HTML reporting layer gives a polished analyst-facing output without adding a frontend framework. TypeScript can be introduced later if a browser UI becomes technically justified.

## 7. CI Design

GitHub Actions tests the actual package installation rather than simply importing files from the checkout. The matrix covers Ubuntu and Windows across Python 3.11–3.14, then runs pytest and the CLI smoke test.

The workflow uses explicit Python versions and current GitHub-maintained setup actions. GitHub's current `setup-python` documentation recommends explicit version selection and supports dependency caching through the action.

The local setup scripts and CI use the same fundamental installation/test contract so that CI failures are more likely to represent real project problems rather than a completely different environment.

## 8. Security Boundary

All Nmap/security testing must remain inside the user's controlled VMware lab and target only the user's Metasploitable VM or other explicitly authorized lab systems.

No conclusion from NetDefender should be presented as broader than the controlled traffic actually tested.
