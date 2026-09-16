# NetDefender Evidence Plan

NetDefender uses evidence to connect a security claim to an observable test result. Development evidence can be generated without the live lab; final network evidence must come from the controlled VMware lab.

## Coding-First Evidence

Before the laptop is needed, capture/reproduce:

- parser tests
- TCP reconnaissance detector tests
- UDP reconnaissance detector tests
- SHA-256/HMAC tests
- HTML report generation test
- synthetic sample analysis
- successful GitHub Actions run

These establish that the software works independently of the VM environment.

## Live Lab Evidence

After the laptop is available:

- VMware view showing Kali and Metasploitable.
- Metasploitable IP configuration.
- Kali IP configuration and route.
- Successful Kali → Metasploitable connectivity test.
- Verified target identity before scanning.
- Nmap command and sanitized output.
- Wireshark/tshark capture showing reconnaissance traffic.
- Exported event data supplied to NetDefender.
- NetDefender detection finding generated from real evidence.
- Cryptographic integrity verification before and after controlled modification.

## Cryptographic Integrity Demonstration

For a controlled evidence artifact:

1. Generate a SHA-256 digest.
2. Generate an HMAC-SHA256 tag using a test secret.
3. Verify the original artifact.
4. Modify the artifact in a controlled test.
5. Verify again and document the failed integrity check.

Secrets used for demonstrations must never be committed to the repository.

## Evidence Naming

Prefer descriptive names such as:

```text
phase1-test-results.txt
phase2-synthetic-detection.json
phase4-integrity-check.txt
phase7-vm-network.png
phase8-nmap-scan.txt
phase8-wireshark-capture.pcapng
phase9-real-detection.json
phase9-integrity-verification.txt
```

## Evidence Rule

A phase is not considered complete because code exists. Software phases should have automated tests; live-lab phases must also be exercised with real controlled traffic and documented evidence.
