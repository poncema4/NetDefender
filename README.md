# NetDefender
**Simulated Enterprise Network Security Environment**

## Overview
NetDefender is a controlled enterprise-network security lab used to design, test, and validate a small defensive network architecture. The MVP combines network segmentation, firewall policy, intrusion detection, VPN access, TLS, and focused cryptographic demonstrations.

NetDefender is intentionally a **security environment/lab**, not one monolithic security application. Each technology has a defined role in the architecture, and the final demonstrations connect those controls through repeatable, observable scenarios.

## Problem
A network can have individual security controls and still be poorly protected if those controls are not connected through a clear architecture. NetDefender tests whether the designed controls behave as intended under controlled network activity and provides packet, alert, firewall, and configuration evidence for the results.

## Objectives
- Design a segmented enterprise network with defined trust zones.
- Enforce traffic policy with pfSense.
- Detect selected suspicious activity with Snort.
- Use Kali Linux and Nmap for controlled reconnaissance and security testing.
- Capture and analyze traffic with Wireshark.
- Demonstrate HTTP versus HTTPS/TLS behavior.
- Demonstrate authenticated and encrypted VPN access.
- Connect cryptographic mechanisms to practical network-security use cases.
- Keep configuration, evidence, and documentation synchronized with the implemented MVP.

## MVP Scope
- Isolated enterprise-style topology with untrusted, DMZ, internal, and VPN zones.
- pfSense firewall rules between zones.
- Snort IDS detection for selected activity.
- Kali/Nmap reconnaissance and testing.
- Wireshark packet captures for evidence.
- TLS certificates and HTTPS using OpenSSL.
- OpenVPN remote-access demonstration.
- Focused demonstrations of hashing, HMAC, public-key cryptography, and digital signatures.
- Repeatable end-to-end security scenarios with documented evidence.

## Architecture / Workflow
```text
                         Untrusted Network
                                |
                           +----------+
                           |  pfSense |
                           | Firewall |
                           +----+-----+
                              / | \
                             /  |  \
                           DMZ Internal VPN
                            |      |     |
                       DMZ Server Internal VPN Client
                                  Client

                         +----------------+
                         |    Snort IDS   |
                         +--------+-------+
                                  |
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

**Tool roles:** pfSense provides routing/firewall policy; Snort provides IDS detection; Kali/Nmap generates controlled security-test traffic; Wireshark provides packet-level evidence; OpenSSL supports certificates/TLS and cryptographic demonstrations; OpenVPN provides remote-access VPN functionality.

## Phase Plan

| Phase | Focus | Status |
|---|---|---|
| 1 | Isolated VirtualBox topology and connectivity | In progress |
| 2 | pfSense firewall policy and segmentation | Planned |
| 3 | DMZ services and controlled targets | Planned |
| 4 | Snort IDS and selected detection rules | Planned |
| 5 | Kali/Nmap testing and Wireshark evidence | Planned |
| 6 | TLS/HTTPS and certificate demonstration | Planned |
| 7 | OpenVPN remote access | Planned |
| 8 | Focused cryptographic demonstrations | Planned |
| 9 | Integrated scenarios, validation, and evidence | Planned |
| 10 | Final documentation, report, and presentation | Planned |

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
| Cryptographic Tools | OpenSSL, GPG |
| Virtualization | Oracle VirtualBox |
| Documentation / Configuration | Markdown, configuration files |
| Version Control | Git / GitHub |

## Project Structure
```text
NetDefender/
├── topology/
│   ├── README.md
│   └── ip-plan.md
├── firewall/
├── ids/
├── vpn/
├── crypto/
├── attacks/
├── captures/
├── evidence/
├── docs/
│   ├── architecture.md
│   └── setup.md
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
Controlled reconnaissance will generate traffic that can be observed in Wireshark and detected by Snort while pfSense enforces the defined network policy. A separate TLS/HTTPS demonstration will show how encryption changes what can be observed in captured traffic. VPN and cryptographic demonstrations will connect authenticated remote access and cryptographic mechanisms to practical network-security use cases.

The final MVP will favor a small number of repeatable scenarios with clear evidence over a large number of loosely connected features.

## Security Scope and Limitations
NetDefender is a local, controlled security laboratory. Testing is limited to the virtual machines and networks created for the project. Kali/Nmap traffic must not target university networks, public IP addresses, third-party systems, or unrelated devices.

The MVP is not intended to represent a complete enterprise SOC, production firewall deployment, or production incident-response platform. Configuration choices will be documented as lab constraints rather than presented as universal production guidance.

## Final MVP Status
The project is currently in **Phase 1: topology and connectivity**. The repository currently contains the project plan and Phase 1 documentation; implementation evidence will be added as each phase is completed.

The final MVP status will be updated throughout implementation. A phase will not be marked complete until its configuration has been implemented, tested, and documented with reproducible evidence.

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

## Verification
Phase-specific verification commands, screenshots, packet captures, firewall evidence, and IDS alerts will be documented as the implementation progresses. Final verification will use repeatable end-to-end scenarios across the completed MVP.

## Documentation
- [Architecture](docs/architecture.md)
- [Setup](docs/setup.md)
- [Topology](topology/README.md)
- [IP Plan](topology/ip-plan.md)
