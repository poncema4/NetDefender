# NetDefender Evidence Plan

NetDefender uses evidence to connect a security claim to an observable test result. Evidence must come from the controlled lab and must not contain unnecessary secrets or personal information.

## Phase 1 Evidence

- VMware view showing Kali and Metasploitable.
- Metasploitable IP configuration.
- Kali IP configuration and route.
- Successful Kali → Metasploitable connectivity test.
- NetDefender repository structure.
- Passing local test run.
- Passing GitHub Actions test run.

## Later Evidence

### Reconnaissance

- Nmap command used.
- Target IP and confirmation that it is the lab target.
- Sanitized Nmap output.
- Wireshark/tshark capture showing relevant traffic.

### Detection

- Input event data.
- Detection rule that matched.
- Generated finding.
- Supporting packet/event fields.

### Cryptographic Integrity

For a controlled evidence artifact:

1. Generate SHA-256 digest.
2. Generate HMAC-SHA256 tag using a test secret.
3. Verify the original artifact.
4. Modify the artifact in a controlled test.
5. Verify again and document the failed integrity check.

Secrets used for demonstrations must never be committed to the repository.

## Evidence Naming

Prefer descriptive names such as:

```text
phase1-vm-network.png
phase1-kali-ip.txt
phase1-metasploitable-ip.txt
phase1-connectivity.png
phase2-nmap-scan.txt
phase2-wireshark-capture.pcapng
phase4-port-scan-detection.json
phase5-evidence-integrity.txt
```

## Evidence Rule

A phase is not considered complete because code exists. The implementation must be exercised, the observed result must be recorded, and the evidence must support the documented claim.
