# NetDefender Setup

## Phase 1 — Isolated Lab + Software Foundation

Phase 1 establishes two things:

1. a working, isolated Kali Linux → Metasploitable network lab; and
2. the software repository foundation that later phases will build into the NetDefender analyzer.

Do not scan anything until the target IP has been verified as the user's own Metasploitable VM.

## Required Software

The MVP is intentionally lightweight:

- VMware Workstation
- Kali Linux
- Metasploitable
- Nmap
- Wireshark (or tshark)
- Python 3
- Git
- GitHub
- GitHub Actions

All listed software is free to use for this project/lab. NetDefender does not require pfSense, Snort, OpenVPN, or a large collection of third-party security products for the MVP.

## Phase 1 Network

```text
┌──────────────┐       isolated VM network       ┌─────────────────┐
│  Kali Linux  │ ──────────────────────────────> │  Metasploitable │
│  Test Source │                                 │     Target      │
└──────────────┘                                 └─────────────────┘
```

The exact IP addresses are recorded only after they are observed from the VMs. Do not invent addresses in the documentation.

## Isolation Requirement

Use a VMware network configuration that keeps NetDefender test traffic inside the intended lab. Prefer an isolated/private VM network for Kali ↔ Metasploitable traffic.

Do not use NetDefender's Nmap tests against:

- university networks
- public IP addresses
- third-party systems
- neighbors' devices
- unrelated host devices

Metasploitable is intentionally vulnerable and should not be exposed to the Internet.

## Phase 1 Procedure

### 1. Start the VMs

Boot Kali Linux and Metasploitable in VMware.

### 2. Verify the Metasploitable address

On Metasploitable, run:

```bash
ifconfig
```

or, if available:

```bash
ip addr
```

Identify the IPv4 address assigned to the lab interface. Record the actual value in `topology/ip-plan.md`.

### 3. Verify Kali networking

On Kali:

```bash
ip addr
ip route
```

Confirm Kali has an interface connected to the same isolated VM network.

### 4. Verify reachability

From Kali, ping the verified Metasploitable address:

```bash
ping -c 4 <METASPLOITABLE_IP>
```

A successful response establishes basic IP connectivity. It does not yet prove that any application service is reachable.

### 5. Confirm the target identity

Before running Nmap, confirm that the address belongs to the Metasploitable VM and is not another system on the network.

### 6. Install/verify Python tooling

On Kali or the development environment:

```bash
python3 --version
python3 -m pip --version
```

Create a virtual environment when implementing the Python application:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 7. Run the initial test suite

After the Phase 1 software skeleton is present:

```bash
python3 -m pytest
```

The expected result is a passing baseline test suite. Later phases will add parser, detection, and cryptography tests.

### 8. Verify GitHub Actions

Push the project to GitHub and confirm the repository's test workflow runs successfully. CI should remain independent of the live Kali/Metasploitable lab; automated tests use deterministic sample data rather than requiring a VM.

## Evidence to Capture

Phase 1 evidence should include:

- VMware view showing the two lab VMs.
- Metasploitable `ifconfig` or `ip addr` output.
- Kali `ip addr` output.
- Kali route information.
- Successful Kali → Metasploitable ping.
- Repository structure showing the NetDefender software foundation.
- Successful GitHub Actions run.

Do not commit passwords, private keys, host-specific secrets, or unnecessary personal/network information.

## Phase 1 Exit Criteria

Phase 1 is complete when:

- Kali and Metasploitable boot successfully.
- Both VMs are connected to the intended isolated network.
- The Metasploitable IP is verified and documented.
- Kali can reach Metasploitable.
- The repository contains the NetDefender application skeleton.
- A deterministic automated test baseline passes locally.
- GitHub Actions verifies the same baseline.
- The isolation boundary is understood.

After these criteria are met, Phase 2 begins with controlled Nmap reconnaissance and evidence collection.
