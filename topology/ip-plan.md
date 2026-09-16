# NetDefender IP Plan

> Populate this file from the running lab. Do not invent or guess addresses.

## Status

**Phase 1: Pending lab verification.**

## Addressing Table

| System | Interface | IPv4 | Network | Status |
|---|---|---|---|---|
| Kali Linux | Lab interface | TBD | Isolated VMware network | Pending |
| Metasploitable | Lab interface | TBD | Isolated VMware network | Pending |

## Verification Commands

### Kali

```bash
ip addr
ip route
```

### Metasploitable

```bash
ifconfig
```

or:

```bash
ip addr
```

### Connectivity

From Kali, after confirming the Metasploitable address:

```bash
ping -c 4 <METASPLOITABLE_IP>
```

## Recording Rule

Only verified values from the running VMware guests should be entered here. This file becomes the source of truth for later Nmap commands, packet captures, fixtures, and final documentation.
