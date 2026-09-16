# NetDefender Setup

## Phase 1 — Isolated Virtual Network

Phase 1 establishes the foundation for the NetDefender MVP. Do not configure the IDS, VPN, TLS demonstrations, or attack scenarios until the base network is verified.

## Required Software

- Oracle VirtualBox
- pfSense virtual machine
- Kali Linux virtual machine
- A small Linux server/client VM for the DMZ
- A small Linux client/server VM for the Internal zone

Additional VPN and service VMs may be added only when required by later phases.

## Phase 1 Topology

```text
Kali Linux
(Untrusted)
     |
     v
  pfSense
  /  |  \\
 v   v   v
DMZ Internal VPN
```

The exact VirtualBox adapter configuration and IP plan are intentionally recorded only after the VMs are created. This prevents documentation from claiming an address or interface that has not been verified.

## Isolation Requirement

The NetDefender lab must use VirtualBox networking that keeps test traffic inside the intended lab. Do not use NetDefender's Kali/Nmap tests against university networks, public IP addresses, third-party systems, or unrelated host devices.

When a VirtualBox adapter is configured for a mode that provides access beyond the isolated lab, document why it is required and ensure test traffic remains limited to authorized lab addresses.

## Phase 1 Procedure

### 1. Create the VMs

Prepare the pfSense, Kali, DMZ, and Internal virtual machines. The VPN role will be connected during the VPN phase; it does not need to be fully implemented in Phase 1.

### 2. Create the lab networks

Create the isolated VirtualBox network segments required to represent the planned trust zones. Record each network name and subnet in `topology/ip-plan.md` once verified.

### 3. Configure pfSense interfaces

Assign the pfSense interfaces to the appropriate trust zones. Record the interface names and addresses from the actual pfSense configuration.

### 4. Configure endpoints

Connect Kali to the Untrusted side and connect the DMZ/Internal systems to their respective networks. Record the actual addresses with commands such as `ip addr` on Linux systems.

### 5. Verify connectivity

From Kali, verify connectivity to the intended pfSense interface. From each endpoint, verify only the connectivity expected at this stage.

At this phase, successful connectivity is only a topology check. Firewall policy will be made explicit in Phase 2.

### 6. Capture evidence

Save screenshots showing:

- VirtualBox network/VM configuration.
- pfSense interface assignments.
- IP configuration on Kali and the other endpoints.
- Connectivity tests.

Do not commit secrets, private keys, passwords, or other sensitive host information.

## Phase 1 Exit Criteria

Phase 1 is complete when:

- The required VMs boot successfully.
- The trust-zone topology is documented.
- pfSense interfaces are assigned and verified.
- Actual IP addressing is documented.
- Kali can reach the intended lab gateway/interface.
- DMZ and Internal endpoints are reachable as intended for the initial topology check.
- Evidence has been captured.
- The lab's isolation boundary is understood.

After these criteria are met, Phase 2 begins with pfSense firewall rules and segmentation.
