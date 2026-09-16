# NetDefender Setup

## Purpose

The software is intentionally built before the live lab is required. This allows the parser, detectors, cryptographic evidence, reporting, and CI to be developed and tested away from the laptop. The laptop is then used to supply real Nmap/Wireshark evidence.

## Development Requirements

- Python 3.11+
- Git
- GitHub
- GitHub Actions

No live VM is required to develop or test the core application.

## Software Development Setup

Clone the repository and enter it:

```bash
git clone https://github.com/poncema4/NetDefender.git
cd NetDefender
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the test dependency:

```bash
python -m pip install -r requirements.txt
```

Run the automated suite:

```bash
python -m pytest
```

Run the synthetic reconnaissance sample:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html report.html
```

This should produce structured findings in the terminal and a dependency-free HTML report.

## Live Lab Setup — Laptop Required

Only after the software is ready:

### 1. Start Kali and Metasploitable

Boot both VMs in VMware Workstation.

### 2. Use an isolated VM network

Connect Kali and Metasploitable to the same private/isolated VMware network. Metasploitable should not be exposed to the Internet.

### 3. Identify Metasploitable

On Metasploitable:

```bash
ifconfig
```

or:

```bash
ip addr
```

Record the actual lab IPv4 address in `topology/ip-plan.md`.

### 4. Verify Kali

On Kali:

```bash
ip addr
ip route
```

### 5. Verify connectivity

From Kali:

```bash
ping -c 4 <METASPLOITABLE_IP>
```

### 6. Confirm target identity

Before any scan, verify that the address is the user's Metasploitable VM.

## Nmap + Wireshark Integration

The live integration phase will use authorized scans such as TCP SYN and UDP reconnaissance against the verified Metasploitable VM.

Wireshark/tshark will capture the resulting traffic. Relevant packet fields will be exported into NetDefender's normalized JSON/CSV event format so the same detection engine used in development can analyze real evidence.

The exact commands and capture filters will be documented after the lab is available and tested.

## Evidence Rules

Do not commit:

- passwords
- private keys
- session tokens
- unrelated host information
- traffic captures containing unnecessary personal information
- scans of systems outside the controlled lab

## Safety Boundary

All Nmap and other security-testing traffic must remain inside the NetDefender lab. Do not target university networks, public IP addresses, third-party systems, neighbors' devices, or unrelated host devices.
