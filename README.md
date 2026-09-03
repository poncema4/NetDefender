# NetDefender

**Simulated Enterprise Network Security Environment**

**Course:** Network Security Engineering & Cryptography  
**Project:** Final MVP / Proof of Concept

## Overview

NetDefender is a controlled enterprise-network security lab used to design, test, and validate a small defensive network architecture. The MVP will combine segmentation, firewall policy, intrusion detection, VPN access, TLS, and cryptographic controls.

## Problem

A network can have individual security controls and still be poorly protected if those controls are not connected through a clear architecture. NetDefender will test whether the designed controls actually behave as intended under controlled network activity.

## Objectives

- Design a segmented enterprise network with defined trust zones.
- Enforce traffic policy with pfSense.
- Detect selected suspicious activity with Snort.
- Use Kali Linux and Nmap for controlled reconnaissance.
- Capture and analyze traffic with Wireshark.
- Demonstrate HTTP versus HTTPS/TLS behavior.
- Demonstrate authenticated and encrypted VPN access.
- Connect cryptographic mechanisms to practical network-security use cases.

## MVP Scope

The MVP will include:

- An isolated enterprise-style topology with untrusted, DMZ, internal, and VPN zones.
- pfSense firewall rules between the zones.
- Snort IDS detection for selected activity.
- Kali/Nmap reconnaissance and testing.
- Wireshark packet captures for evidence.
- TLS certificates and HTTPS using OpenSSL.
- OpenVPN remote-access demonstration.
- Focused demonstrations of hashing, HMAC, public-key cryptography, and digital signatures where relevant.

## Architecture / Workflow

```text
Untrusted Network
        ↓
     pfSense
   ↙    ↓    ↘
 DMZ  Internal  VPN
   \    ↓    /
     Snort IDS
        ↓
   Monitoring
```

```text
Build Network
     ↓
Run Controlled Test
     ↓
Capture Traffic
     ↓
Detect Activity
     ↓
Enforce Policy
     ↓
Review Evidence
```

## Tech Stack

- **Firewall / Routing:** pfSense
- **IDS/IPS:** Snort
- **Testing Platform:** Kali Linux
- **Reconnaissance:** Nmap
- **Traffic Analysis:** Wireshark
- **TLS / Certificates:** OpenSSL
- **VPN:** OpenVPN
- **Cryptographic Tools:** OpenSSL and GPG where useful
- **Virtualization:** Oracle VirtualBox
- **Documentation / Configuration:** Markdown and configuration files
- **Version Control:** Git / GitHub

## Project Structure

```text
NetDefender/
├── topology/
├── firewall/
├── ids/
├── vpn/
├── crypto/
├── attacks/
├── captures/
├── evidence/
├── docs/
└── README.md
```

## Security Concepts

- Symmetric and public-key cryptography
- Hashing and HMAC
- Digital signatures
- PKI and certificates
- TLS/HTTPS
- Network segmentation
- Firewalls
- IDS/IPS
- VPNs
- Defense in depth
- Least privilege
- Network security testing

## Expected Demonstration

A controlled reconnaissance attempt will generate network traffic that can be observed in Wireshark and detected by Snort, while pfSense enforces the defined network policy. A separate TLS/HTTPS demonstration will show how encryption changes what can be observed in captured traffic.

All testing will remain inside the isolated lab environment.

## Out of Scope

- Internet-facing deployment
- Large enterprise/SOC infrastructure
- Full SIEM implementation
- Internet-wide scanning
- Testing third-party networks
- Fully automated incident response
- Large-scale wireless deployment
- Generic security scoring

## Future Enhancements

- Additional network zones and VLANs
- More Snort rules
- Centralized logging
- Additional VPN and TLS scenarios
- Controlled MITM/replay demonstrations
- IPsec demonstrations
- Expanded cryptographic key-management workflows

## Status

Planned MVP. Implementation will begin with the isolated topology, trust zones, and firewall policy.