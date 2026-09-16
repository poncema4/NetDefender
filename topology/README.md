# NetDefender Phase 1 Topology

## Goal

Establish the smallest controlled network needed to generate real network-security evidence while keeping the main deliverable coding-focused.

## Current Lab

```text
┌──────────────────────┐
│      Kali Linux      │
│  Authorized Tester   │
│      Nmap tools      │
└──────────┬───────────┘
           │
           │ isolated VMware network
           │
┌──────────▼───────────┐
│    Metasploitable    │
│   Authorized Target  │
│ intentionally vuln. │
└──────────────────────┘
```

This two-VM topology is sufficient for the MVP. Additional infrastructure will only be added if a later security scenario requires it.

## Roles

| System | Role | Purpose |
|---|---|---|
| Kali Linux | Test source | Nmap reconnaissance and controlled security testing |
| Metasploitable | Test target | Intentionally vulnerable target for authorized lab traffic |
| VMware | Isolation layer | Keeps the test environment separated from unrelated systems |
| NetDefender | Analysis platform | Parses evidence, detects activity, protects evidence integrity, and reports findings |

## IP Plan

See [ip-plan.md](ip-plan.md). Addresses are recorded only after being verified from the running VMs.

## Phase 1 Exit Criteria

- Both VMs boot.
- Both VMs use the intended isolated VMware network.
- Metasploitable's IP is verified.
- Kali's IP and route are verified.
- Kali can reach Metasploitable.
- No test traffic is directed outside the lab.
- NetDefender's software foundation and CI baseline pass.
