# NetDefender

**Simulated Enterprise Network Security & Cryptography Environment**

> **Course:** Network Security Engineering & Cryptography  
> **Project Type:** Final Course MVP / Proof of Concept  
> **Status:** Planned MVP

## Overview

NetDefender is a controlled network-security laboratory designed to demonstrate how secure enterprise network architecture, cryptography, monitoring, detection, and defensive controls work together.

The project will model a small enterprise environment with separated network zones, firewall controls, intrusion detection, secure remote access, encrypted communications, and controlled security testing.

The central question is:

> **Does the secure network architecture actually detect, contain, and defend against controlled attacks?**

Rather than producing a generic security score, NetDefender will demonstrate security through network behavior: traffic is generated, observed, detected, and either permitted or blocked according to the architecture and defensive controls.

## Course

**Seton Hall University — Network Security Engineering & Cryptography**

NetDefender is designed around the course topics involving cryptographic foundations, TLS/HTTPS, PKI, network architecture, segmentation, firewalls, IDS/IPS, VPNs, Wireshark traffic analysis, controlled MITM/replay scenarios, wireless security concepts, OpenSSL/GPG, and network security testing with tools such as Nmap and Kali.

## Problem

A network can contain individual security controls and still be poorly designed if those controls are not connected through a coherent architecture.

NetDefender addresses this by creating a small simulated enterprise network and then testing whether its architecture and controls behave as intended under controlled attack scenarios.

The project emphasizes the relationship between:

```text
Network Architecture
        ↓
Security Control
        ↓
Observed Traffic
        ↓
Attack / Test
        ↓
Detection
        ↓
Defense / Mitigation
```

## Project Goal

The goal of NetDefender is to build a functional proof of concept of a secure enterprise network environment and validate its design through controlled testing.

The MVP should demonstrate:

1. Network segmentation.
2. Firewall policy enforcement.
3. Intrusion detection.
4. Secure remote connectivity through VPN concepts.
5. Encrypted communication using TLS/HTTPS.
6. Packet and protocol analysis with Wireshark.
7. Controlled reconnaissance and attack traffic using Kali/Nmap.
8. Cryptographic operations and certificate/key concepts using appropriate tools.
9. Evidence that the defensive controls change or detect the resulting network behavior.

## MVP Scope

The MVP will intentionally model a small enterprise environment rather than attempting to reproduce a large production network.

### 1. Enterprise Network Segmentation

The environment will contain logically separated network zones such as:

- Internet / untrusted network
- DMZ
- Internal enterprise network
- VPN access path

Segmentation will be used to demonstrate how network placement and access rules reduce unnecessary exposure between systems.

### 2. Firewall

A firewall will enforce traffic policies between the simulated network zones.

The MVP will demonstrate rules such as:

- Allowed traffic to intentionally exposed services.
- Restricted traffic between network zones.
- Blocked unauthorized access attempts.
- Controlled administrative access.

The objective is to show policy enforcement as part of the network architecture rather than simply displaying firewall configuration.

### 3. Intrusion Detection

An IDS/IPS component such as Snort will monitor relevant traffic and identify selected suspicious or malicious patterns.

The MVP will demonstrate at least one controlled attack or reconnaissance scenario that generates detectable traffic.

Expected flow:

```text
Kali / Test Host
       ↓
Controlled Network Activity
       ↓
Firewall / Network Path
       ↓
Snort Detection
       ↓
Alert / Defensive Action
```

### 4. Network Traffic Analysis

Wireshark will be used to inspect and explain network traffic generated during the demonstrations.

The project will use packet captures to demonstrate concepts such as:

- TCP/IP communication
- HTTP versus HTTPS
- TLS negotiation
- DNS or other relevant protocol behavior
- Reconnaissance traffic
- Detection-related traffic patterns

The goal is to connect the abstract security concept to the actual packets traveling through the network.

### 5. TLS / HTTPS

The environment will include a secure web-communication demonstration using TLS certificates and HTTPS.

The project will demonstrate how cryptographic protection changes what an observer can learn from network traffic compared with unencrypted HTTP.

Where appropriate, OpenSSL will be used to inspect or create certificates and cryptographic material in the controlled environment.

### 6. VPN

The MVP will demonstrate secure remote connectivity using a VPN technology such as OpenVPN.

The demonstration will show the difference between a direct untrusted connection and authenticated/encrypted access through the VPN path.

### 7. Cryptography Demonstration

NetDefender will include focused cryptographic demonstrations relevant to the network environment.

Potential demonstrations include:

- Symmetric encryption concepts
- Public-key cryptography
- Hashing
- HMAC
- Digital signatures
- Certificate validation
- Key generation and management concepts
- OpenSSL operations
- GPG operations where useful

The cryptography component will be connected to real network-security use cases rather than existing as a disconnected collection of command-line exercises.

### 8. Controlled Security Testing

Kali Linux and Nmap will be used to conduct controlled reconnaissance and security testing against the isolated lab environment.

Potential demonstrations include:

- Host discovery
- Port scanning
- Service enumeration
- Suspicious traffic generation
- Controlled attack scenarios relevant to the architecture

All testing will remain within the intentionally isolated lab environment.

## Planned Architecture

The initial architecture is expected to resemble:

```text
                         Untrusted Network
                                |
                                v
                         +--------------+
                         |    pfSense   |
                         |   Firewall   |
                         +--------------+
                           /     |      \
                          /      |       \
                         v       v        v
                      DMZ    Internal     VPN
                       |      Network      |
                       |         |         |
                       v         v         v
                    Web/App   Internal   Remote
                    Services  Services    User
                         \       |        /
                          \      |       /
                           +-----+------+
                                 |
                                 v
                            Snort IDS/IPS
                                 |
                                 v
                         Security Monitoring

Kali / Test Host → Controlled Attack Traffic → Network → Detection / Defense
```

The exact topology and virtualization implementation will be finalized during MVP development.

## Attack-and-Defense Model

NetDefender will use controlled attacks to validate the defensive architecture.

A representative demonstration will follow this pattern:

```text
1. Establish secure network architecture
              ↓
2. Generate controlled reconnaissance
              ↓
3. Observe traffic with Wireshark
              ↓
4. Detect activity with Snort
              ↓
5. Enforce firewall policy where applicable
              ↓
6. Review evidence
              ↓
7. Explain mitigation and architectural impact
```

This approach makes the project demonstrable: the network is not merely configured; it is tested.

## Cryptography and Network Security Relationship

A central design goal is to show that cryptography is part of network security architecture rather than a separate topic.

Examples include:

```text
TLS
 ↓
Confidentiality + Integrity + Authentication
 ↓
Secure Application Communication
```

and:

```text
VPN
 ↓
Authenticated / Encrypted Tunnel
 ↓
Protected Remote Network Access
```

The project will use these relationships to explain why cryptographic mechanisms matter to the network as a whole.

## Course Concepts Demonstrated

The MVP is intended to demonstrate practical understanding of:

- Symmetric cryptography
- AES concepts
- Public-key cryptography
- RSA / ECC concepts
- Hashing
- SHA
- HMAC
- Digital signatures
- PKI
- TLS
- HTTPS
- Certificate creation and validation
- Secure network architecture
- Network segmentation
- Defense in depth
- Firewalls
- IDS/IPS
- Snort
- VPNs
- OpenVPN
- Wireshark
- Kali Linux
- Nmap
- Controlled MITM/replay concepts where appropriate
- Secure wireless concepts where appropriate
- OpenSSL
- GPG
- Network security auditing

## Design Principles

### Controlled Environment

All attack and testing activity will occur within a deliberately isolated lab environment. The project is not intended to test third-party networks.

### Defense in Depth

Security will not depend on a single control. Segmentation, firewall policy, encryption, detection, and authentication will work together.

### Observable Security

Every major demonstration should produce evidence that can be inspected through packets, logs, alerts, firewall decisions, certificates, or other technical artifacts.

### Architecture Before Tools

Tools such as pfSense, Snort, Wireshark, Kali, and Nmap will support the architecture rather than becoming the architecture themselves.

### Small, Complete MVP

The project will prioritize a small network that can be fully configured, attacked, observed, defended, and explained rather than a large topology that cannot be completed reliably.

## Expected Demonstration

A final MVP demonstration should show a complete scenario such as:

1. Present the enterprise network architecture.
2. Explain the trust zones and firewall policies.
3. Establish secure remote access through the VPN.
4. Generate controlled reconnaissance from Kali.
5. Observe the resulting traffic in Wireshark.
6. Show the corresponding IDS detection.
7. Demonstrate firewall enforcement where applicable.
8. Compare protected and unprotected network communication using TLS/HTTPS.
9. Inspect certificate or cryptographic evidence.
10. Explain how the controls work together to protect the simulated enterprise.

## Out of Scope for the MVP

The initial proof of concept will intentionally avoid unnecessary enterprise complexity.

The following are not required for the MVP:

- Large-scale production network deployment
- Internet-facing infrastructure
- Enterprise SIEM deployment
- Full SOC automation
- Dozens of VLANs or network segments
- Comprehensive vulnerability scanning across the Internet
- Real-world third-party penetration testing
- Complete wireless enterprise deployment
- Advanced automated incident response
- A generic security score

Additional capabilities may be considered after the core network is functional.

## Future Enhancements

Potential future enhancements include:

- More network zones and VLANs
- Additional Snort rules
- Automated alert collection
- Centralized logging
- Expanded VPN scenarios
- Additional TLS/certificate experiments
- More advanced Nmap testing
- Controlled MITM/replay demonstrations
- Wireless security lab components
- IPsec demonstrations
- More detailed cryptographic key-management workflows
- Additional attack-and-defense scenarios

These enhancements are secondary to completing the core MVP.

## Development Philosophy

NetDefender will be developed incrementally. The priority is to create one complete attack-and-defense path before expanding the environment.

Every implemented component should answer a concrete security question and produce evidence that can be inspected and explained.

The final MVP should demonstrate not only that security tools were configured, but that the resulting architecture behaves differently when security controls are correctly applied.

## Academic Context

This repository represents the project concept and implementation for **Network Security Engineering & Cryptography**. It is intended to demonstrate an original proof of concept applying network architecture, defensive engineering, cryptography, and controlled security testing to a simulated enterprise environment.

Implementation, testing, documentation, and final presentation materials will be developed as the project progresses.
