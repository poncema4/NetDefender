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
│  Input → Parser → Normalizer → Detection Engine        │
│                              │                         │
│                              v                         │
│                 Findings + Evidence                    │
│                              │                         │
│                              v                         │
│                 SHA-256 + HMAC                         │
│                              │                         │
│                              v                         │
│                    HTML / JSON Report                  │
└───────────────────────────┬────────────────────────────┘
                            v
                    GitHub Actions CI
```

## 3. Core Components

### 3.1 Network Event Model

`NetworkEvent` provides a stable representation of observed traffic: timestamp, source/destination addresses, protocol, ports, TCP flags, and packet length. Detection rules do not depend on the original capture format.

### 3.2 Input Parser

The parser accepts JSON and CSV event data. This gives the project a deterministic test interface before real packet captures are introduced. Later lab work can export relevant Wireshark/tshark fields into the same model.

### 3.3 Detection Engine

The first detection rules target observable reconnaissance behavior:

- `NET-RECON-001`: burst of TCP SYN probes to many destination ports.
- `NET-RECON-002`: burst of UDP probes to many destination ports.

Rules are intentionally deterministic and explainable. A finding records the rule, source, target, severity, port evidence, packet count, and observation window.

### 3.4 Cryptographic Evidence

SHA-256 creates a deterministic digest of an evidence artifact. HMAC-SHA256 demonstrates integrity/authenticity when a shared secret is available. Verification uses constant-time comparison for the HMAC check.

The crypto layer is connected to the detection workflow: NetDefender produces evidence, then creates and verifies cryptographic metadata for that evidence.

### 3.5 Reporting

The MVP generates JSON findings and a dependency-free HTML report. A TypeScript browser interface remains a possible later enhancement, but it will only be added if it improves the final demonstration without distracting from network security.

## 4. Current Software Flow

```text
JSON/CSV events
      ↓
Parser
      ↓
NetworkEvent objects
      ↓
TCP/UDP reconnaissance rules
      ↓
Finding objects
      ↓
JSON + HTML report
      ↓
Evidence digest / HMAC verification
```

## 5. Phase Organization

The phases are intentionally ordered so all coding that can be completed away from the laptop happens first. The physical lab work comes after the software is ready.

| Phase | Focus | Work location | Status |
|---|---|---|---|
| 1 | Software architecture + data model | Anywhere | **Complete foundation** |
| 2 | Parser + validation | Anywhere | **Implemented** |
| 3 | Detection engine | Anywhere | **Implemented** |
| 4 | Cryptographic evidence | Anywhere | **Implemented** |
| 5 | Reporting / analyst output | Anywhere | **Implemented** |
| 6 | Automated testing + GitHub Actions | Anywhere | **Implemented / expanding** |
| 7 | VMware lab setup | Laptop | Pending |
| 8 | Real Nmap + Wireshark integration | Laptop | Pending |
| 9 | End-to-end validation + evidence | Laptop | Pending |
| 10 | Final report + presentation | Anywhere | Pending |

## 6. Design Decisions

### Why Python?

Python keeps parsing, detection, cryptography, reporting, and testing in one cohesive codebase. It also minimizes installation burden on the lab machine.

### Why not add many enterprise products?

pfSense, Snort, OpenVPN, and similar systems can demonstrate useful concepts, but using all of them would turn the project into an infrastructure-configuration project. NetDefender instead uses a small controlled lab and puts the engineering depth into the software itself.

### Why not add another language immediately?

A second language is useful only when it solves a real project problem. The current dependency-free HTML reporting layer gives a polished analyst-facing output without adding a frontend framework. TypeScript can be introduced later if a browser UI becomes technically justified.

## 7. Security Boundary

All Nmap/security testing must remain inside the user's controlled VMware lab and target only the user's Metasploitable VM or other explicitly authorized lab systems.
