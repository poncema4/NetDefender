# NetDefender Topology

This directory documents the isolated virtual network used by the NetDefender MVP.

## Phase 1 Goal

Build and verify a small enterprise-style network in Oracle VirtualBox before adding firewall policy, IDS, VPN, TLS, and cryptographic demonstrations.

## Planned Trust Zones

| Zone | Purpose | Initial Role |
|---|---|---|
| Untrusted | Security-testing side of the lab | Kali Linux |
| DMZ | Public-facing services in the simulated enterprise | DMZ server |
| Internal | Trusted enterprise systems | Internal client/server |
| VPN | Remote-access path into the enterprise | VPN client |
| Firewall | Routing and policy boundary | pfSense |

## Phase 1 Network Model

```text
                 Kali Linux
               (Untrusted Zone)
                      |
                      |
                 [ pfSense ]
                /     |      \
               /      |       \
            DMZ    Internal     VPN
             |         |          |
        DMZ Server  Internal   VPN Client
                    Client
```

The exact IP addressing will be recorded after the virtual interfaces are created and verified. No addresses are invented in this document.

## Phase 1 Verification

Before Phase 2 begins, verify:

1. Every planned VM exists and has the expected virtual network adapter(s).
2. pfSense boots and exposes the expected interfaces.
3. Kali can reach the intended pfSense interface.
4. The DMZ and Internal systems receive addresses from the intended network configuration.
5. Traffic between zones is understood before firewall policy is added.
6. The lab remains isolated from networks and systems that are not part of NetDefender.

## Evidence to Capture

- VirtualBox VM list showing the NetDefender lab VMs.
- pfSense interface assignments.
- IP configuration from each relevant VM.
- Connectivity test from Kali to pfSense.
- Connectivity tests between intended lab endpoints.
- Final Phase 1 topology diagram with actual IP addresses.

## Security Boundary

NetDefender is a controlled lab. Testing will be limited to the virtual machines and networks created for this project. Kali/Nmap testing must not target university networks, public IP addresses, third-party systems, or other devices outside the lab.
