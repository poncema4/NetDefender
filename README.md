# NetDefender

**Simulated Enterprise Network Security & Cryptography Environment**

**Course:** Network Security Engineering & Cryptography  
**Project:** Final Course MVP / Proof of Concept  
**Status:** Planned

## 1. Project Overview

NetDefender is a controlled network-security laboratory that models a small enterprise environment and validates its security architecture through controlled testing.

The project will combine network segmentation, firewall policy, intrusion detection, secure remote access, TLS, cryptographic operations, packet analysis, and reconnaissance testing into one coherent environment.

The central question is:

> **Does the network architecture behave as intended when it is tested under controlled attack conditions?**

The MVP will focus on building a small network that can be configured, tested, observed, and defended. It will not attempt to reproduce a full enterprise SOC or production network.

## 2. Course Alignment

NetDefender is designed for **Seton Hall University — Network Security Engineering & Cryptography**.

The project directly connects to course topics including:

- Symmetric and asymmetric cryptography
- AES concepts
- RSA/ECC concepts
- Hashing and HMAC
- Digital signatures
- PKI and certificate management
- TLS/HTTPS
- Network architecture and segmentation
- Firewalls
- IDS/IPS
- VPNs
- Wireshark traffic analysis
- Kali Linux
- Nmap
- OpenSSL
- GPG
- Controlled MITM/replay concepts where appropriate
- Network security auditing

## 3. Problem Statement

Individual network-security tools do not automatically produce a secure network. A firewall, IDS, VPN, or encrypted protocol must operate within an architecture that defines trust boundaries, permitted communication, and defensive responsibilities.

NetDefender will address this by building a small simulated enterprise network and then testing the architecture from the perspective of both an administrator and a controlled attacker.

The project will connect architecture to observable evidence:

```text
Network Architecture
        ↓
Security Policy
        ↓
Controlled Test / Attack
        ↓
Network Traffic
        ↓
Detection / Enforcement
        ↓
Evidence and Analysis
```

## 4. Project Objectives

The MVP will aim to:

1. Design a small enterprise network with meaningful trust zones.
2. Implement firewall rules between those zones.
3. Deploy intrusion detection for selected suspicious activity.
4. Provide secure remote access through a VPN.
5. Demonstrate encrypted application traffic using TLS/HTTPS.
6. Generate and inspect certificates/cryptographic material with OpenSSL where appropriate.
7. Capture and analyze network traffic with Wireshark.
8. Use Kali Linux and Nmap for controlled reconnaissance.
9. Produce technical evidence showing how the defensive controls respond to the tests.

## 5. MVP Scope

### 5.1 Network Segmentation

The initial topology will contain a small number of zones with distinct security purposes:

- **Untrusted / external network**
- **DMZ** for intentionally exposed services
- **Internal enterprise network**
- **VPN access path** for remote users

The goal is to demonstrate that systems do not all share the same trust level and that communication between zones is explicitly controlled.

### 5.2 Firewall Policy

A pfSense firewall will control traffic between the simulated zones.

The MVP will include policies for:

- Permitted public-facing services
- Restricted DMZ-to-internal communication
- Controlled administrative access
- Blocked unauthorized connections
- VPN access to selected internal resources

The important result is not simply the existence of firewall rules; it is evidence that the rules affect what traffic is permitted.

### 5.3 Intrusion Detection

Snort will monitor selected network traffic and identify controlled reconnaissance or suspicious activity.

The initial demonstration will use a small number of detection scenarios that can be reproduced reliably.

```text
Kali / Test Host
       ↓
Controlled Reconnaissance
       ↓
Network Traffic
       ↓
Snort
       ↓
Alert / Defensive Response
```

### 5.4 Traffic Analysis

Wireshark will provide packet-level evidence for the demonstrations.

The project will inspect traffic such as:

- TCP/IP communication
- HTTP and HTTPS
- TLS negotiation
- DNS where relevant
- Port scanning/reconnaissance
- Traffic associated with IDS alerts

The objective is to explain what is happening on the network rather than treating the tools as black boxes.

### 5.5 TLS / HTTPS

A service in the simulated environment will use HTTPS with a certificate generated or inspected using OpenSSL.

The project will compare encrypted and unencrypted communication where appropriate to demonstrate what TLS protects and what a packet observer can actually see.

### 5.6 VPN

OpenVPN will provide a controlled remote-access scenario.

The demonstration will show how an authenticated, encrypted tunnel changes the path and protection of remote network access compared with an untrusted direct connection.

### 5.7 Cryptography

Cryptography will be demonstrated in the context of network security rather than as a disconnected set of exercises.

The MVP may include:

- Symmetric encryption
- Public-key cryptography
- Hashing
- HMAC
- Digital signatures
- Certificate generation and validation
- Key generation and management concepts
- OpenSSL operations
- GPG operations where they directly support the demonstration

The final selection will be kept small enough to explain each operation clearly.

### 5.8 Controlled Reconnaissance

Kali Linux and Nmap will be used only against the isolated lab environment.

The initial tests may include:

- Host discovery
- Port scanning
- Service enumeration
- Controlled suspicious traffic
- Security-control validation

The purpose is to validate the network architecture, not to perform unrestricted penetration testing.

## 6. Planned Architecture

The initial design will follow a small enterprise-style topology:

```text
                         External / Untrusted Network
                                      |
                                      v
                               +-------------+
                               |   pfSense   |
                               |   Firewall  |
                               +-------------+
                                /      |      \
                               /       |       \
                              v        v        v
                            DMZ     Internal     VPN
                             |       Network      |
                             |          |         |
                             v          v         v
                          Web/App   Internal    Remote
                          Service   Services     User
                              \        |        /
                               \       |       /
                                +------+------+
                                       |
                                       v
                                  Snort IDS/IPS
                                       |
                                       v
                                Alert / Evidence

        Kali / Test Host → Controlled Activity → Network → Detection / Defense

        Wireshark → Packet Capture / Protocol Analysis
        OpenSSL   → Certificates / Cryptographic Operations
```

The exact virtual-machine and interface configuration will be finalized during implementation.

## 7. Tech Stack

| Area | Technology | Purpose |
|---|---|---|
| Firewall / Router | **pfSense** | Network segmentation and policy enforcement |
| IDS/IPS | **Snort** | Detection of selected suspicious network activity |
| Attacker / Test Host | **Kali Linux** | Controlled reconnaissance and security testing |
| Traffic Analysis | **Wireshark** | Packet capture and protocol analysis |
| Network Discovery | **Nmap** | Host discovery, port scanning, and service enumeration |
| TLS / Certificates | **OpenSSL** | Certificate and cryptographic operations |
| File / Message Cryptography | **GPG** | Selected encryption/signature demonstrations |
| VPN | **OpenVPN** | Secure remote network access |
| Virtualization | **VirtualBox** | Isolated laboratory infrastructure where appropriate |
| Configuration | **pfSense/Snort configuration files and documented rules** | Reproducible network/security setup |
| Documentation | **Markdown** | Architecture, procedures, findings, and evidence |

Unlike the other two projects, NetDefender will not require a traditional web frontend/backend application for its MVP. The primary product is the **network environment and its observable security behavior**.

## 8. Planned Repository Structure

The repository will organize the network design, configurations, testing procedures, and evidence by responsibility.

```text
NetDefender/
├── architecture/
│   ├── diagrams/
│   ├── topology/
│   └── addressing/
├── firewall/
│   └── pfsense/
├── ids/
│   └── snort/
├── vpn/
│   └── openvpn/
├── crypto/
│   ├── openssl/
│   └── gpg/
├── testing/
│   ├── nmap/
│   ├── wireshark/
│   └── attack-scenarios/
├── evidence/
├── docs/
└── README.md
```

The exact files and configuration format will be established during implementation. The structure is intended to keep architecture, defensive configuration, cryptography, testing, and evidence clearly separated.

## 9. Attack-and-Defense Validation

The project will validate the network through controlled scenarios.

A representative test will follow this sequence:

```text
1. Configure the network architecture
              ↓
2. Establish firewall and IDS controls
              ↓
3. Generate controlled reconnaissance from Kali
              ↓
4. Capture the traffic with Wireshark
              ↓
5. Observe Snort detection
              ↓
6. Verify firewall enforcement where applicable
              ↓
7. Record technical evidence
              ↓
8. Explain the architectural control that produced the result
```

This approach makes the network demonstrable. The environment is not only configured; it is challenged and validated.

## 10. Cryptography in the Network

A major goal is to connect cryptographic mechanisms to the network services they protect.

### TLS / HTTPS

```text
Certificate + Public-Key Cryptography
                ↓
               TLS
                ↓
Encrypted Application Traffic
                ↓
Confidentiality + Integrity + Authentication
```

### VPN

```text
Authentication + Encryption
          ↓
     VPN Tunnel
          ↓
Protected Remote Access
```

### Integrity / Authentication

Hashing, HMAC, signatures, and certificates will be used where they help explain real security properties of network communication.

## 11. Security Principles

### Defense in Depth

The environment will rely on multiple controls: segmentation, firewall policy, encryption, VPN access, and intrusion detection.

### Explicit Trust Boundaries

Network zones will have defined security purposes and communication between zones will be controlled.

### Observable Security

Major demonstrations should produce evidence in the form of packets, alerts, firewall decisions, certificates, logs, or other technical artifacts.

### Architecture Before Tools

pfSense, Snort, Wireshark, Kali, and Nmap are implementation and validation tools. The network security architecture comes first.

### Controlled Testing

All attack and reconnaissance activity will remain inside the intentionally isolated laboratory.

## 12. Expected Demonstration

The final MVP should support a concise end-to-end demonstration:

1. Present the enterprise topology and trust zones.
2. Explain the firewall policy.
3. Establish VPN access.
4. Show HTTPS/TLS configuration and certificate evidence.
5. Launch controlled reconnaissance from Kali.
6. Observe the resulting packets in Wireshark.
7. Show the corresponding Snort detection.
8. Demonstrate firewall enforcement where applicable.
9. Review the evidence.
10. Explain how the controls work together as a layered defense.

## 13. Out of Scope for the MVP

The first version will intentionally avoid unnecessary enterprise complexity.

Out of scope:

- Internet-facing production infrastructure
- Large enterprise topology
- Full SOC/SIEM deployment
- Large-scale automated incident response
- Dozens of network segments
- Internet-wide vulnerability scanning
- Testing third-party networks
- Complete enterprise wireless deployment
- Advanced automated attack orchestration
- A generic security score

## 14. Future Enhancements

If time permits after the core MVP is stable, possible additions include:

- Additional VLANs and trust zones
- More Snort rules
- Centralized logging
- Expanded VPN scenarios
- Additional TLS/certificate experiments
- IPsec
- Controlled MITM/replay demonstrations
- Wireless security scenarios
- More detailed key-management workflows
- Additional attack-and-defense cases

These enhancements are secondary to the core architecture and validation workflow.

## 15. Project Definition

NetDefender is a **network-security engineering proof of concept**. The project will demonstrate that a secure network is the result of architecture, policy, cryptographic protection, monitoring, and testing working together.

The finished MVP should provide enough technical evidence to answer three questions:

1. **How was the network designed to be secure?**
2. **What happened when the design was tested?**
3. **What evidence shows that the defensive controls worked?**

That is the basis of the project's final proof of concept.