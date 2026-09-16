# NetDefender Rules and Project Contract

This document defines the rules that keep NetDefender technically coherent, reproducible, safe, and honest about what the project demonstrates.

## 1. Detection Rules

The detection engine currently implements two deterministic reconnaissance rules.

| Rule | Name | Trigger | Default threshold | Severity |
|---|---|---|---|---|
| `NET-RECON-001` | TCP SYN reconnaissance | One source sends TCP SYN probes to many destination ports on one target inside a short window | 10 distinct ports / 10 seconds | Medium |
| `NET-RECON-002` | UDP reconnaissance | One source sends UDP probes to many destination ports on one target inside a short window | 8 distinct ports / 10 seconds | Medium |

### NET-RECON-001 — TCP SYN reconnaissance

The rule looks for TCP events where protocol is TCP, a destination port is present, TCP flags contain SYN but not ACK, the same source/target pair contacts at least 10 distinct destination ports, and the observations occur within a 10-second window.

This corresponds to a recognizable SYN-scan pattern such as an authorized Nmap `-sS` experiment. It is not a claim that every SYN scan will always satisfy these exact thresholds.

Evidence includes distinct destination ports, packet count, and observation window.

### NET-RECON-002 — UDP reconnaissance

The rule looks for UDP events where a destination port is present, the same source/target pair contacts at least 8 distinct destination ports, and the observations occur within a 10-second window.

This provides a deterministic software representation of a controlled UDP reconnaissance experiment such as an authorized Nmap `-sU` scan.

Evidence includes distinct destination ports, packet count, and observation window.

## 2. Rule Design Requirements

Every future detection rule must:

1. Have a unique `NET-*` identifier.
2. State exactly what packet/event fields it consumes.
3. Use explicit thresholds rather than unexplained magic behavior.
4. Produce explainable evidence.
5. Have positive tests that prove detection.
6. Have negative tests that prove important non-detections.
7. Be deterministic for the same input.
8. Avoid depending on wall-clock time during analysis.
9. Avoid external services.
10. Be documented here before becoming part of the supported detection contract.

## 3. False-Positive Rules

NetDefender must not call every unusual packet malicious.

A finding means the observed event set matched a documented NetDefender detection condition. It does **not** automatically mean the source is malicious.

Controlled experiments, administrators, vulnerability scanners, monitoring systems, and legitimate testing can generate reconnaissance-like traffic.

Thresholds are detection conditions, not universal definitions of an attack.

## 4. Input Rules

Supported inputs are JSON normalized events, CSV normalized events, and PCAP/PCAPNG through the tshark adapter when tshark is installed.

All inputs must become `NetworkEvent` objects before detection.

Detection rules must not contain format-specific parsing logic. Parsing belongs in the parser/capture layers.

## 5. Evidence Rules

Every finding should retain enough evidence for an analyst to understand why the rule fired.

For reconnaissance rules this includes, as applicable:

- source IP;
- destination IP;
- destination ports;
- packet count;
- observation window;
- rule identifier.

Cryptographic evidence may be used to demonstrate that an evidence artifact changed after it was recorded.

## 6. Cryptography Rules

### SHA-256

Use SHA-256 as a deterministic digest of an evidence artifact.

### HMAC-SHA256

Use HMAC-SHA256 when demonstrating integrity/authentication with a shared secret.

Secrets must never be committed to the repository. Tests may use clearly labeled test-only secrets that do not represent production credentials.

### Verification

Verification must check both the artifact and its associated cryptographic metadata. The application must not report an artifact as verified merely because a manifest file exists.

## 7. Report Rules

JSON output is the machine-readable representation. HTML output is the analyst-friendly representation.

Reports must distinguish observed data, generated findings, cryptographic verification state, and limitations.

Reports must not claim that a finding proves compromise, attribution, intent, or universal detection coverage.

## 8. Testing Rules

Every functional change should include an appropriate automated test.

At minimum, a detection rule should have:

- one positive case;
- one below-threshold case;
- one case that resembles the pattern but should not trigger because of a relevant protocol/flag distinction;
- deterministic evidence assertions.

Crypto changes should test valid verification, modified artifact rejection, modified metadata rejection where applicable, and deterministic digest behavior.

Parser changes should test valid input, malformed input, timestamp normalization, numeric conversion, and missing optional fields.

CLI changes should test the entry point through the same command users are expected to run.

## 9. CI Rules

The main branch is considered healthy only when the latest commit's CI succeeds.

CI must validate more than a single happy-path test run. The supported matrix covers Ubuntu, Windows, Python 3.11–3.14, package installation, pytest, CLI smoke execution, and report generation.

If CI fails, the failure must be read and understood. Re-running a failing job without addressing the underlying defect is not considered a fix.

A test should never be weakened solely to make CI green.

## 10. Local/CI Parity Rules

The preferred local validation command is:

```bash
python -m pytest
```

The preferred package installation is:

```bash
python -m pip install -e ".[test]"
```

CI should use the same package/test contract whenever possible.

Platform-specific behavior must be handled explicitly rather than hidden behind CI-only workarounds.

## 11. Dependency Rules

The core application intentionally has no runtime third-party dependencies. The test environment uses pytest.

A new runtime dependency should only be added when it solves a real engineering requirement that cannot reasonably be handled by the standard library or existing architecture.

Adding libraries solely to increase the technology count is against the project design.

## 12. Language Rules

Python is the primary implementation language.

A second language such as TypeScript may be added only when it provides a concrete architectural benefit, such as a justified analyst UI.

A second language must not be added simply to make a project slide list longer.

## 13. External Tool Rules

| Tool | Role |
|---|---|
| VMware Workstation | Controlled virtualization |
| Kali Linux | Authorized test host |
| Metasploitable | Controlled vulnerable target |
| Nmap | Generates authorized reconnaissance traffic |
| Wireshark/tshark | Captures/inspects traffic |
| GitHub Actions | Reproducible CI |

NetDefender remains the primary software engineering artifact.

## 14. Lab Safety Rules

All security testing must remain inside the user's controlled lab.

Never target public IP addresses, university networks, third-party servers, neighbors' devices, unrelated devices on the host network, or systems without explicit authorization.

Metasploitable should remain isolated because it is intentionally vulnerable.

## 15. Evidence Collection Rules

For every real lab experiment, record:

1. Experiment identifier.
2. Date/time.
3. Kali IP.
4. Metasploitable IP.
5. Exact Nmap command.
6. Nmap output.
7. Wireshark/tshark capture filename.
8. NetDefender command.
9. NetDefender findings.
10. Cryptographic verification result.
11. Required screenshots.
12. Limitations or unexpected behavior.

Never invent an observation that was not actually produced by the lab.

## 16. Documentation Rules

Documentation must match the code currently on `main`.

When a command, path, threshold, supported Python version, or workflow changes, update the relevant documentation in the same change set.

The setup guide should be understandable to someone cloning the repository for the first time.

## 17. Git Rules

For this project, direct changes to `main` are intentional.

Do not introduce a pull-request workflow merely for process overhead.

Every commit should leave the repository in a coherent state. Do not knowingly leave `main` broken while moving on to unrelated work.

## 18. Definition of Done

A software phase is complete only when its implementation, tests, documentation, and CI behavior agree.

For the coding-first milestone, all of the following are required:

- parser implemented;
- detection engine implemented;
- crypto evidence implemented;
- reporting implemented;
- automated tests implemented;
- setup scripts implemented;
- setup documentation implemented;
- CI covers supported platforms/versions;
- latest commit passes CI;
- no known CI failure is being ignored;
- no known error-log defect is being hidden by changing a test to something meaningless.

## 19. Phase Boundary

Phase 1 is the architecture/data-model foundation and is complete.

Phases 2–5 are implemented in the current software.

Phase 6 is the automated testing/CI milestone and is complete only after the latest commit is verified green.

Phase 7 starts the physical VMware lab work.

The project is not fully finished until the live lab, real packet evidence, end-to-end validation, and final submission materials are complete.
