# NetDefender

**Simulated Enterprise Network Security Environment**

**Course:** Network Security Engineering & Cryptography  
**Project:** Final MVP / Proof of Concept

## Overview

NetDefender is a controlled enterprise-network security lab used to design, test, and validate a small defensive network architecture.

The MVP will combine network segmentation, firewall policy, intrusion detection, VPN access, TLS, and cryptographic controls. Kali Linux will be used for controlled reconnaissance and testing, while Wireshark and Snort will provide evidence of what happened on the network.

The project is focused on **attack-and-defense validation**, not on producing a security score.

## Project Goal

The main question NetDefender addresses is:

> **Does the network architecture actually detect and defend against the activity it was designed to protect against?**

The MVP will build a small isolated enterprise environment and then test its controls with repeatable scenarios.

## MVP Scope

- Design a segmented enterprise network with an untrusted side, DMZ, internal network, and VPN access path.
- Use **pfSense** to enforce traffic policy between zones.
- Use **Snort** to detect selected suspicious activity.
- Use **Kali Linux / Nmap** for controlled reconnaissance and security testing.
- Use **Wireshark** to capture and explain network behavior.
- Demonstrate **HTTP vs. HTTPS/TLS** traffic.
- Use **OpenSSL** for certificate and cryptographic operations.
- Demonstrate authenticated/encrypted remote access with **OpenVPN**.
- Use selected cryptographic concepts such as hashing, HMAC, public-key cryptography, and digital signatures where they directly support the network demonstrations.

## Planned Architecture

```text
                 Untrusted Network
                        |
                        v
                  +-----------+
                  |  pfSense  |
                  |  Firewall |
                  +-----------+
                   /    |    \
                  /     |     \
                DMZ  Internal  VPN
                 |      |       |
                 +------+-------+
                        |
                        v
                    Snort IDS
                        |
                        v
                    Monitoring

Kali / Nmap → Controlled Traffic → Network → Detection / Defense
```

The exact topology will be finalized during implementation, but the network will remain isolated from unrelated systems.

## Tech Stack

| Area | Technology |
|---|---|
| Firewall / Routing | pfSense |
| IDS/IPS | Snort |
| Testing Platform | Kali Linux |
| Reconnaissance | Nmap |
| Traffic Analysis | Wireshark |
| TLS / Certificates | OpenSSL |
| VPN | OpenVPN |
| Cryptographic Tools | OpenSSL, GPG where useful |
| Virtualization | Oracle VirtualBox |
| Documentation / Configuration | Markdown, configuration files |
| Version Control | Git / GitHub |

Unlike the other projects, NetDefender does not require a traditional frontend/backend application. The primary system is the network environment and the evidence produced by its controls.

## Planned Repository Structure

```text
NetDefender/
├── topology/
├── firewall/
├── ids/
├── vpn/
├── crypto/
├── captures/
├── attacks/
├── evidence/
├── docs/
└── README.md
```

The repository will keep network configuration, attack scenarios, packet captures, evidence, and documentation separated by purpose.

## Attack-and-Defense Demonstration

A successful MVP demonstration should follow a clear path:

```text
Build Secure Network
        ↓
Run Controlled Reconnaissance
        ↓
Capture Traffic with Wireshark
        ↓
Detect Activity with Snort
        ↓
Enforce Firewall Policy
        ↓
Review Evidence
        ↓
Explain the Defense
```

A separate TLS demonstration will show how encrypted communication changes what can be observed in a packet capture.

## Course Alignment

NetDefender applies the course material on cryptography, PKI, TLS/HTTPS, network architecture, segmentation, firewalls, IDS/IPS, VPNs, Wireshark, Kali, Nmap, OpenSSL, GPG, and controlled attack/defense testing.

## Security Principles

- **Segmentation:** limit unnecessary communication between trust zones.
- **Defense in depth:** use multiple controls rather than relying on one device.
- **Least privilege:** allow only required network access.
- **Encryption:** protect communications and remote access.
- **Detection:** produce evidence when suspicious activity occurs.
- **Validation:** test the architecture instead of assuming the controls work.

## Out of Scope

- Internet-facing deployment
- Large enterprise/SOC infrastructure
- Full SIEM implementation
- Internet-wide scanning
- Testing third-party networks
- Fully automated incident response
- Large-scale wireless deployment
- Generic security scoring

## Status

This repository currently defines the project and MVP. Implementation will begin with the isolated topology, trust zones, and firewall policy, followed by detection and attack/defense testing.
