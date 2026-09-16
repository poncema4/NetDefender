# NetDefender Setup Guide

This guide is the source of truth for setting up the **NetDefender software locally** and, later, connecting it to the controlled VMware security lab.

## 1. What You Are Setting Up

NetDefender has two deliberately separate environments:

1. **Software environment** — Python, the NetDefender package, pytest, Git, and optional tshark for real PCAP analysis.
2. **Controlled network lab** — VMware Workstation, Kali Linux, and Metasploitable.

The software environment does **not** require the VMs. You can build, test, generate reports, and run the synthetic sample on a normal Linux or Windows computer.

The VMware lab is only required when we move from deterministic development data to real Nmap/Wireshark evidence.

The project intentionally avoids unnecessary infrastructure products. NetDefender is the primary software project; Kali, Metasploitable, Nmap, and Wireshark/tshark provide the controlled laboratory traffic and evidence.

---

## 2. Supported Development Platforms

| Platform | Core development | Real PCAP parsing | VMware lab |
|---|---|---|---|
| Ubuntu/Linux | Supported | Supported with tshark | Supported |
| Windows | Supported | Supported with tshark | Supported |
| macOS | Not the primary documented target | Possible | Not part of the documented lab |

The repository requires **Python 3.11 or newer**. The CI matrix currently exercises Python 3.11, 3.12, 3.13, and 3.14 on both Ubuntu and Windows.

GitHub's current `setup-python` documentation recommends explicitly selecting a Python version instead of relying on whatever happens to be preinstalled on a runner. NetDefender follows that approach in CI.

---

## 3. Fastest Setup: Linux

From a terminal in the repository root:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The script:

1. Finds a usable Python 3.11+ interpreter.
2. Creates `.venv` if it does not exist.
3. Upgrades pip inside the virtual environment.
4. Installs NetDefender in editable mode with the test dependency.
5. Runs the complete pytest suite.
6. Runs the deterministic CLI sample.
7. Writes `local-report.html` as a smoke-test artifact.
8. Reports whether `tshark` is available without making tshark mandatory for core development.

Activate the environment later with:

```bash
source .venv/bin/activate
```

Then normal development is:

```bash
python -m pytest
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

---

## 4. Fastest Setup: Windows PowerShell

Open PowerShell in the repository root and run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

The script performs the Windows equivalent of the Linux setup:

1. Finds Python 3.11+.
2. Creates `.venv` if necessary.
3. Upgrades pip in that virtual environment.
4. Installs NetDefender and its test dependency.
5. Runs pytest.
6. Runs the deterministic CLI sample.
7. Creates `local-report.html`.
8. Reports whether tshark is installed.

Activate the environment later with:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell script execution is restricted, the `Set-ExecutionPolicy -Scope Process ...` command above changes policy only for the current PowerShell process.

---

## 5. Manual Linux Setup

If you do not want to use the script:

### Check Python

```bash
python3 --version
```

You need Python 3.11 or newer.

### Clone the repository

```bash
git clone https://github.com/poncema4/NetDefender.git
cd NetDefender
```

### Create the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the project

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

### Run tests

```bash
python -m pytest
```

### Run the synthetic sample

```bash
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

---

## 6. Manual Windows Setup

Check Python:

```powershell
py --version
```

or:

```powershell
python --version
```

Clone and enter the repository:

```powershell
git clone https://github.com/poncema4/NetDefender.git
Set-Location NetDefender
```

Create and activate the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

Test:

```powershell
python -m pytest
```

Run the sample:

```powershell
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

---

## 7. What Is Required vs Optional

### Required for software development

- Git
- Python 3.11+
- Internet access for the initial Python package installation
- A shell/terminal

### Required for automated CI

Nothing additional on your computer. GitHub Actions creates its own environment.

### Optional for real PCAP work

- Wireshark/tshark

NetDefender does not add a Python packet-processing dependency just to read PCAP files. The real-capture adapter invokes `tshark` and converts selected packet fields into the same normalized event model used by the rest of the application.

### Required only for the live lab

- VMware Workstation
- Kali Linux VM
- Metasploitable VM
- An isolated VMware network
- Nmap inside Kali
- Wireshark/tshark where capture/export is performed

---

## 8. Installing tshark on Ubuntu

For the real PCAP phase:

```bash
sudo apt update
sudo apt install tshark
```

Verify:

```bash
tshark --version
```

During installation Ubuntu may ask whether non-root users should be allowed to capture packets. For this project, packet capture should remain limited to the controlled lab interface. The NetDefender PCAP adapter itself reads an existing capture file, so live capture privileges are not required for the application.

---

## 9. Installing Wireshark/tshark on Windows

Install Wireshark using its official Windows installer and ensure the command-line `tshark.exe` component is installed.

Then open a new PowerShell window and verify:

```powershell
tshark --version
```

If PowerShell cannot find `tshark`, either add the Wireshark installation directory to PATH or invoke tshark using its full path. NetDefender should not require hard-coded machine-specific paths.

---

## 10. Project Smoke Test

After installation, this command should work without VMware:

```bash
python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
```

Expected behavior:

- the sample parses successfully;
- the TCP SYN reconnaissance rule produces a finding;
- structured output is printed;
- `local-report.html` is created;
- the HTML file is non-empty.

The exact finding is deterministic because the input sample is synthetic and version-controlled.

---

## 11. Real PCAP Smoke Test

Once tshark is installed, NetDefender can analyze a PCAP/PCAPNG file through the CLI:

```bash
python -m netdefender.cli path/to/capture.pcap --html pcap-report.html
```

The PCAP adapter extracts only the fields needed by the normalized `NetworkEvent` model:

- frame timestamp;
- source IP;
- destination IP;
- protocol;
- source port;
- destination port;
- TCP flags;
- packet length.

If tshark is unavailable, the command should fail with an actionable message rather than silently pretending that a PCAP was analyzed.

---

## 12. Controlled VMware Lab Setup

Do this **after** the software setup and automated tests are working.

### 12.1 Start the VMs

Start:

- Kali Linux — authorized test host
- Metasploitable — intentionally vulnerable target

### 12.2 Isolate the network

Put both VMs on the same isolated/private VMware network.

Do not bridge Metasploitable onto a normal home, university, public, or production network.

Metasploitable is intentionally vulnerable. Treat it as an untrusted machine.

### 12.3 Identify Metasploitable's address

On Metasploitable:

```bash
ip addr
```

or:

```bash
ifconfig
```

Record the actual lab IP in `topology/ip-plan.md`.

### 12.4 Identify Kali's address and route

On Kali:

```bash
ip addr
ip route
```

Confirm the two VMs share the expected isolated subnet.

### 12.5 Verify connectivity

From Kali:

```bash
ping -c 4 <METASPLOITABLE_IP>
```

Do not proceed until the address is confirmed to be the Metasploitable VM.

---

## 13. Nmap Rules for This Project

Every security scan must satisfy all of these conditions:

1. The target must be the user's Metasploitable VM or another explicitly authorized lab machine.
2. The target address must be verified immediately before scanning.
3. The scan must remain on the isolated lab network.
4. Do not use NetDefender commands against public IP addresses.
5. Do not scan university infrastructure.
6. Do not scan neighbors' or other people's devices.
7. Do not scan unrelated host machines merely because they are reachable.
8. Save scan output so the result can be compared with captured traffic.
9. Record the exact Nmap command used.
10. Record the target IP and timestamp.
11. Capture the corresponding traffic when the experiment calls for packet evidence.
12. Do not present a controlled-lab observation as proof of universal network behavior.

---

## 14. Recommended Development Order

Use this order so the project stays coding-first:

```text
1. Clone repository
2. Run setup script
3. Run pytest
4. Run synthetic CLI sample
5. Inspect generated HTML report
6. Install tshark only when PCAP work begins
7. Configure VMware lab
8. Verify Kali ↔ Metasploitable connectivity
9. Run one authorized Nmap experiment
10. Capture traffic
11. Analyze the PCAP with NetDefender
12. Compare Nmap result ↔ packet evidence ↔ NetDefender finding
13. Repeat for additional scan types
14. Preserve evidence and screenshots
```

---

## 15. Troubleshooting

### `python3: command not found`

Install Python 3.11+ using the operating system's package manager or official Python distribution, then rerun the setup script.

### Python exists but is too old

Check:

```bash
python3 --version
```

NetDefender requires 3.11+.

### `venv` creation fails on Ubuntu

Install the matching Python venv package, for example:

```bash
sudo apt install python3-venv
```

Then rerun the setup script.

### `pytest` cannot be found

Do not install it globally. Activate `.venv` and run:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

### `No module named netdefender`

Make sure the virtual environment is active and the repository root is the current directory. Then run:

```bash
python -m pip install -e ".[test]"
```

### `tshark` cannot be found

Verify:

```bash
tshark --version
```

If it is not installed, install Wireshark/tshark for the operating system. Core JSON/CSV development does not require tshark.

### PCAP analysis says tshark is missing

This is an environment problem, not a reason to bypass the adapter. Install tshark and rerun the same command.

### Tests fail

Do not simply rerun the job until it turns green. Read the failing test and traceback, determine whether the defect is in implementation, test expectations, packaging, or environment setup, fix the underlying problem, and rerun the complete suite.

### GitHub Actions fails while local tests pass

Check:

1. the Python version used by the failing matrix entry;
2. operating-system differences;
3. path handling;
4. shell behavior;
5. packaging/install behavior;
6. the exact failing traceback.

The goal is a genuinely portable project, not a CI-only workaround.

---

## 16. Evidence and Git Rules

Do not commit:

- passwords;
- private keys;
- HMAC secrets;
- session tokens;
- unrelated PCAPs;
- personal traffic captures;
- scans from outside the controlled lab;
- machine-specific absolute paths;
- generated virtual environments;
- generated reports unless they are intentionally part of the submission evidence.

Before committing a new experiment, ask:

- What exact security question was tested?
- What was the authorized target?
- What command generated the traffic?
- What packet evidence was captured?
- What did NetDefender detect?
- What did it not detect?
- What limitations apply?

---

## 17. CI Philosophy

The CI pipeline is intentionally stricter than a single `pytest` invocation. It should validate:

- supported Python versions;
- Linux behavior;
- Windows behavior;
- package installation;
- the complete automated test suite;
- the CLI entry point;
- deterministic sample processing;
- HTML report creation.

The CI configuration uses explicit Python versions and the current GitHub-maintained checkout/setup actions. This follows GitHub's documented approach to reproducible Python setup.

A green CI result means the tested software contract passed. It does **not** mean the VMware lab has been validated yet.

---

## 18. Definition of Done for the Software Milestone

The coding-first milestone is not considered complete merely because a GitHub Actions job turns green once.

It is complete when:

- the failing tests have been understood and fixed at the correct layer;
- the full suite passes;
- the package installs cleanly;
- the CLI works;
- the synthetic sample works;
- the report is generated;
- Linux and Windows CI pass across the supported Python matrix;
- setup scripts are usable;
- documentation matches the actual repository;
- the repository contains no accidental secrets or machine-specific assumptions;
- the latest commit itself has a successful CI run.

After that point, the project moves into the live-lab phases rather than continuing to add software merely for the sake of adding software.

---

## 19. Phase Transition

The coding-first phases are:

| Phase | Status |
|---|---|
| 1 — Architecture + data model | Complete |
| 2 — Parser + validation | Implemented |
| 3 — Detection engine | Implemented |
| 4 — Cryptographic evidence | Implemented |
| 5 — Reporting | Implemented |
| 6 — Automated testing + CI | Complete only after the latest commit passes the full CI matrix |
| 7 — VMware lab setup | Next physical-lab phase |

Phase 1 is therefore already complete. The remaining question before calling the **coding-first milestone** complete is Phase 6 verification on the latest commit. Phase 7 begins only after that verification is genuinely green.
