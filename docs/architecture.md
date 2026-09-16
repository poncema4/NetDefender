# NetDefender Architecture

## 1. Purpose

NetDefender is a controlled network-security laboratory backed by a purpose-built analysis application. It is designed for ISCI 6101: Network Security Engineering & Cryptography.

The architecture deliberately keeps the number of external systems small. VMware, Kali, and Metasploitable provide the isolated environment; Nmap and Wireshark/tshark generate and expose network evidence; NetDefender provides the primary coding and analysis work.

## 2. High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    ISOLATED VM LAB                          │
│                                                             │
│   ┌───────────────┐       controlled       ┌──────────────┐ │
│   │   Kali Linux  │ ─────── Nmap ─────────>│Metasploitable│ │
│   │ Test / Source │       traffic           │    Target    │ │
│   └───────────────┘                         └──────┬───────┘ │
│                                                    │         │
│                         packet capture             │         │
│                              ┌─────────────────────┘         │
│                              v                               │
│                       Wireshark / tshark                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ pcap / structured events
                               v
┌─────────────────────────────────────────────────────────────┐
│                       NETDEFENDER                           │
│                                                             │
│  Input → Parser → Normalizer → Detector → Finding Report   │
│                              │                              │
│                              v                              │
│                    Evidence Integrity                       │
│                     SHA-256 + HMAC                          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               v
                       Tests + CI Validation
                         GitHub Actions
```

## 3. Core Components

### 3.1 Lab Environment

VMware provides the virtualization layer. Kali is the authorized test source and Metasploitable is the intentionally vulnerable target. The virtual network must be isolated so generated traffic cannot accidentally reach unrelated systems.

### 3.2 Traffic Collection

Nmap is used to create repeatable reconnaissance traffic. Wireshark or tshark is used to inspect and capture that traffic. Packet captures and derived structured data become controlled input to NetDefender.

### 3.3 Event Parser

The parser converts raw or structured network observations into a consistent internal representation. The first implementation will prioritize useful fields such as:

- timestamp
- source IP
- destination IP
- source port
- destination port
- transport protocol
- TCP flags when available
- packet/event type

The parser should reject malformed input cleanly rather than silently creating misleading events.

### 3.4 Detection Engine

The first detector will focus on reconnaissance/port-scanning behavior. Detection logic should be deterministic and explainable.

A finding should identify:

- what was detected
- source and target
- relevant ports/protocols
- evidence supporting the detection
- detection rule used
- timestamp/window where applicable
- confidence or severity only when the value has a documented meaning

The project will avoid pretending that one heuristic can detect every form of malicious traffic.

### 3.5 Cryptographic Evidence

NetDefender will use SHA-256 to create a deterministic digest of evidence and HMAC to demonstrate integrity/authenticity when a shared secret is available.

The application will support an explicit verification operation so a captured evidence file can be checked before and after controlled modification.

Cryptography is part of the design rather than a separate demo pasted onto the project: the detector produces evidence, and the crypto layer protects the integrity of that evidence.

### 3.6 Reporting

The MVP will generate a readable report containing detections, supporting network evidence, and integrity metadata. A lightweight TypeScript UI may be added later if it materially improves presentation; it is not required for the core engine.

## 4. Data Flow

```text
Nmap scan
   ↓
Captured packets / exported events
   ↓
Parser
   ↓
Normalized NetworkEvent objects
   ↓
Detection rules
   ↓
Finding objects
   ↓
Evidence serialization
   ↓
SHA-256 / HMAC
   ↓
Report
```

## 5. Design Decisions

### Why Python?

Python is the core implementation language because it keeps packet/data parsing, detection logic, cryptography, and automated testing cohesive. The goal is substantial engineering rather than a collection of languages.

### Why allow TypeScript?

A small TypeScript frontend can be introduced if the final report/dashboard benefits from a browser interface. It remains optional so the project does not become a frontend-development project instead of a network-security project.

### Why not pfSense/Snort/OpenVPN for the MVP?

Those are valuable enterprise technologies, but adding them all would shift the project toward infrastructure configuration and create a much larger dependency footprint. NetDefender instead focuses on a smaller number of controls that can be implemented, tested, explained, and demonstrated in depth.

## 6. Phase Plan

1. **Isolated lab + software foundation** — configure Kali/Metasploitable networking and establish the Python project structure and CI baseline.
2. **Reconnaissance collection** — run controlled Nmap scenarios and save sanitized evidence.
3. **Traffic parsing** — implement event models, parsers, validation, and normalization.
4. **Detection engine** — implement and test reconnaissance detection rules.
5. **Cryptographic evidence** — add SHA-256/HMAC generation and verification.
6. **Reporting/UI** — create a useful security report and optionally a small TypeScript interface.
7. **Testing + CI** — expand automated tests and enforce repeatable verification through GitHub Actions.
8. **Integration** — execute end-to-end lab scenarios and collect final evidence.
9. **Submission** — finalize documentation, report, presentation, and reproducibility instructions.

## 7. Security Boundary

All test traffic must remain inside the controlled NetDefender lab. The target IPs used by Nmap must be verified as the user's own Metasploitable VM before scanning.
