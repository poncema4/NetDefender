# NetDefender Evidence Plan

NetDefender evidence connects a documented security question to an observable result. The final evidence should show the controlled traffic, the captured packets, the NetDefender analysis, and the resulting report without overstating what the detector proves.

## Software Evidence

The software evidence includes:

- parser and normalization tests;
- TCP reconnaissance detector tests;
- UDP reconnaissance detector tests;
- SHA-256 and HMAC-SHA256 tests;
- evidence-manifest tampering tests;
- HTML report generation tests;
- deterministic sample analysis;
- successful GitHub Actions validation.

The current automated suite passes 17/17 tests.

## Real Lab Evidence

The validated controlled lab evidence includes:

- Kali Linux at `172.16.198.129`;
- Metasploitable at `172.16.198.128`;
- Nmap-generated TCP reconnaissance traffic;
- Nmap-generated UDP reconnaissance traffic;
- Wireshark packet-capture evidence;
- NetDefender analysis of the corresponding PCAP/PCAPNG files;
- TCP positive detection;
- UDP positive detection;
- TCP below-threshold control with no finding;
- HTML reports for the TCP positive, UDP positive, and TCP control cases.

## Validated TCP Positive Result

Capture:

```text
tcp-syn-scan-001.pcapng
```

Command:

```bash
sudo nmap -sS -p 1-100 172.16.198.128
```

NetDefender produced one:

```text
NET-RECON-001
TCP SYN reconnaissance pattern detected
Source: 172.16.198.129
Target: 172.16.198.128
Distinct destination ports: 1–100
```

## Validated TCP Control Result

Capture:

```text
tcp-control-001.pcapng
```

NetDefender output:

```text
[]
```

The HTML report states:

```text
No findings were generated for the supplied evidence.
```

This is the negative validation case showing that below-threshold traffic does not produce a TCP reconnaissance finding.

## Validated UDP Positive Result

Capture:

```text
udp-scan-001.pcapng
```

Command:

```bash
sudo nmap -sU -p 1-20 172.16.198.128
```

NetDefender produced one:

```text
NET-RECON-002
UDP reconnaissance pattern detected
Source: 172.16.198.129
Target: 172.16.198.128
Distinct destination ports: 1–20
Packet count: 87
Observation window: 10 seconds
```

## HTML Reports

The final controlled-lab report set is:

```text
tcp-syn-scan-001-report.html
udp-scan-001-report.html
tcp-control-001-report.html
```

The positive reports demonstrate detection. The control report demonstrates non-detection.

## Cryptographic Evidence

The cryptographic layer demonstrates controlled evidence integrity:

1. Compute a SHA-256 digest of an evidence artifact.
2. Compute an HMAC-SHA256 tag using a test-only secret.
3. Build a manifest containing the cryptographic metadata and findings.
4. Verify the original artifact.
5. Modify the artifact in a controlled test.
6. Verify again and confirm that verification fails.

Secrets used for demonstrations must never be committed to the repository.

## Evidence Interpretation

A finding is a deterministic match against the documented NetDefender rule conditions. It is not proof of compromise, malicious intent, attribution, or universal detection coverage.

The strongest presentation connects:

```text
Nmap command
    ↓
Actual packets
    ↓
Wireshark capture
    ↓
PCAP/PCAPNG
    ↓
NetDefender analysis
    ↓
Finding / no finding
    ↓
HTML report
```

## Evidence Handling

Keep final lab evidence outside the source repository unless an artifact is intentionally included for course submission.

Do not commit:

- passwords or private keys;
- HMAC secrets;
- personal traffic captures;
- unrelated captures;
- scans from outside the controlled lab;
- machine-specific generated files;
- virtual environments.

Never invent a result that was not produced by the controlled experiment.
