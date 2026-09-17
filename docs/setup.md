# NetDefender Setup Guide

This guide explains how to install NetDefender, run the automated tests, use the CLI, analyze real PCAP/PCAPNG evidence, and connect the application to the controlled VMware lab.

## 1. Software Requirements

- Python 3.11 or newer
- Git
- A terminal or PowerShell
- TShark for real PCAP/PCAPNG analysis
- VMware Workstation only for the controlled lab
- Kali Linux and Metasploitable only for the controlled lab

The core JSON/CSV workflow does not require TShark or VMware.

## 2. Clone the Repository

```bash
git clone https://github.com/poncema4/NetDefender.git
cd NetDefender
```

## 3. Linux Setup

From the repository root:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The script creates `.venv`, upgrades pip, installs NetDefender with its test dependency, runs the complete test suite, runs the deterministic sample, generates `local-report.html`, and reports whether TShark is available.

Activate the environment later with:

```bash
source .venv/bin/activate
```

Then run:

```bash
python -m pytest
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

## 4. Windows Setup

From PowerShell in the repository root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

Activate later with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python -m pytest
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

## 5. Manual Python Setup

### Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest
```

### Windows

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest
```

## 6. TShark for Real PCAP Analysis

Verify TShark:

```bash
tshark --version
```

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install tshark
```

On Windows, install Wireshark with the TShark command-line component and verify that `tshark.exe` is available on PATH.

NetDefender reads an existing capture through TShark. The application does not require live packet-capture privileges.

## 7. CLI Usage

Analyze a JSON or CSV event file:

```bash
python -m netdefender.cli data/samples/syn-scan.json
```

Generate an HTML report at the same time:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

Analyze a real PCAP/PCAPNG file:

```bash
python -m netdefender.cli /path/to/capture.pcapng
```

Generate an HTML report from a real capture:

```bash
python -m netdefender.cli /path/to/capture.pcapng --html report.html
```

If the input format cannot be inferred from the extension, use the CLI `--format` option.

## 8. Controlled VMware Lab

The lab should remain isolated/private.

```text
Kali Linux
   │
   │ Nmap
   ▼
Metasploitable
   │
   │ captured traffic
   ▼
Wireshark / TShark
   │
   ▼
PCAP/PCAPNG
   │
   ▼
NetDefender
```

Before testing:

1. Start Kali and Metasploitable.
2. Put both VMs on the isolated VMware network.
3. Confirm each VM's IP address.
4. Confirm the target is the Metasploitable VM.
5. Verify Kali can reach the target.
6. Start packet capture when the experiment requires it.
7. Run only the authorized Nmap command for the experiment.
8. Save the capture and preserve the exact command used.

Never bridge Metasploitable onto a normal home, university, production, or public network.

## 9. Current Controlled Lab Addresses

The validated lab uses:

| System | Interface | Address |
|---|---|---|
| Kali Linux | `eth1` | `172.16.198.129/24` |
| Metasploitable | `eth0` | `172.16.198.128/24` |
| Ubuntu VMware host | `vmnet1` | `172.16.198.1/24` |
| Ubuntu VMware host | `vmnet8` | `172.16.250.1/24` |

Verify the addresses on the machines before an experiment rather than relying only on documentation.

## 10. Controlled TCP Demonstration

On Kali, capture traffic on `eth1` with Wireshark and run the authorized scan against the verified Metasploitable address:

```bash
sudo nmap -sS -p 1-100 172.16.198.128
```

Save the resulting capture as:

```text
tcp-syn-scan-001.pcapng
```

Analyze it from the NetDefender environment:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/tcp-syn-scan-001.pcapng
```

Generate the report:

```bash
python -m netdefender.cli \
  /home/kali/NetDefender-evidence/tcp-syn-scan-001.pcapng \
  --html /home/kali/NetDefender-evidence/tcp-syn-scan-001-report.html
```

The validated capture produced one `NET-RECON-001` finding with destination ports 1–100.

## 11. TCP Control Demonstration

Use the below-threshold control capture:

```text
/home/kali/NetDefender-evidence/tcp-control-001.pcapng
```

Run:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/tcp-control-001.pcapng
```

Expected result:

```text
[]
```

An HTML report can also be generated:

```bash
python -m netdefender.cli \
  /home/kali/NetDefender-evidence/tcp-control-001.pcapng \
  --html /home/kali/NetDefender-evidence/tcp-control-001-report.html
```

The validated control report states that no findings were generated.

## 12. Controlled UDP Demonstration

On Kali, capture traffic on `eth1` and run the authorized UDP scan against the verified Metasploitable address:

```bash
sudo nmap -sU -p 1-20 172.16.198.128
```

Save the resulting capture as:

```text
udp-scan-001.pcapng
```

Analyze it:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/udp-scan-001.pcapng
```

Generate the report:

```bash
python -m netdefender.cli \
  /home/kali/NetDefender-evidence/udp-scan-001.pcapng \
  --html /home/kali/NetDefender-evidence/udp-scan-001-report.html
```

The validated capture produced one `NET-RECON-002` finding with destination ports 1–20 and a packet count of 87 within the documented 10-second observation window.

## 13. Verification Commands

Run the automated suite:

```bash
python -m pytest
```

Run the deterministic sample:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

Run a real capture:

```bash
python -m netdefender.cli /path/to/capture.pcapng --html report.html
```

## 14. Troubleshooting

### Python is missing or too old

```bash
python3 --version
```

NetDefender requires Python 3.11+.

### Virtual environment creation fails on Ubuntu

Install the matching venv package:

```bash
sudo apt install python3-venv
```

### pytest is missing

Activate `.venv` and install the test extra:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

Use `python -m pytest` rather than a globally installed pytest executable so the active virtual environment is used.

### TShark is missing

```bash
tshark --version
```

Install Wireshark/TShark for the operating system before attempting PCAP analysis.

### PCAP analysis fails

Confirm:

- the capture path is correct;
- TShark is installed and on PATH;
- the capture is readable;
- the virtual environment is active;
- the target PCAP came from the controlled lab.

Do not silently substitute synthetic data for a failed real-capture analysis.

### GitHub Actions fails

Read the failing matrix job and traceback. Check Python version, operating system, package installation, path handling, shell behavior, and test output. Fix the underlying issue rather than weakening the test.

## 15. Security and Evidence Handling

Do not commit:

- passwords;
- private keys;
- HMAC secrets;
- session tokens;
- personal traffic captures;
- unrelated PCAPs;
- scans from outside the controlled lab;
- machine-specific absolute paths;
- virtual environments;
- generated reports unless intentionally included as submission evidence.

Keep controlled evidence outside the source tree when possible. The current lab evidence path used during validation is `/home/kali/NetDefender-evidence/`.

## 16. Git Workflow

After a documentation or code change is pushed to GitHub:

```bash
cd ~/NetDefender
git pull origin main
```

For normal development:

```bash
git add .
git commit -m "Describe the change"
git push origin main
```

Keep PCAP evidence outside the repository unless a specific submission artifact is intentionally version-controlled.
