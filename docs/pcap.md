# Real PCAP Analysis

NetDefender can analyze PCAP/PCAPNG captures through the optional TShark adapter in `netdefender/capture.py`.

## TShark fields

The adapter extracts:

- `frame.time_epoch` — packet timestamp
- `ip.src` — source IPv4 address
- `ip.dst` — destination IPv4 address
- `ip.proto` — numeric IP protocol identifier
- `tcp.srcport` — TCP source port when present
- `tcp.dstport` — TCP destination port when present
- `tcp.flags` — numeric TCP flag bitmask when present
- `frame.len` — packet length

The adapter intentionally uses `ip.proto` rather than Wireshark's `_ws.col.Protocol` display-column field. Display-column rendering can vary by TShark version/context and may be empty when requested through `-T fields`.

## Protocol normalization

The numeric IP protocol values used by the adapter are:

| IP protocol | NetDefender protocol |
|---:|---|
| `1` | `ICMP` |
| `6` | `TCP` |
| `17` | `UDP` |

Known protocol names supplied by tests/callers are preserved. Other non-empty protocol values are retained in normalized uppercase form; missing values become `UNKNOWN`.

## TCP flag normalization

TShark may return TCP flags as a numeric bitmask. NetDefender converts the bitmask into stable flag names before creating `NetworkEvent` objects. For example:

- `0x0002` → `SYN`
- `0x0012` → `SYN,ACK`

This allows the detection engine to use the same deterministic `SYN`/`ACK` logic for synthetic events and real captures.

## Controlled lab workflow

For the VMware lab, keep the capture on the isolated Kali/Metasploitable network:

```text
Kali (Nmap)
    ↓
Metasploitable
    ↓
Wireshark/TShark capture
    ↓
PCAP/PCAPNG
    ↓
NetDefender TShark adapter
    ↓
NetworkEvent
    ↓
Detection engine
    ↓
Evidence/report
```

A Wireshark display filter such as:

```text
ip.addr == 172.16.198.128 && tcp.flags.syn == 1
```

changes what Wireshark displays; it does not by itself mean that only those displayed packets were written to a capture file. For NetDefender validation, an unfiltered capture is preferable because it preserves the complete packet context.

## PCAP smoke test

With TShark installed and the repository virtual environment active:

```bash
python -m netdefender.cli /path/to/capture.pcapng
```

For the current controlled SYN-scan experiment:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/tcp-syn-scan-001.pcapng
```

To inspect the parsed events directly:

```bash
python -c "from pathlib import Path; from netdefender.capture import parse_pcap; e=parse_pcap(Path('/home/kali/NetDefender-evidence/tcp-syn-scan-001.pcapng')); print('Events:', len(e)); print('Protocols:', sorted(set(x.protocol for x in e))); print('SYN:', sum(x.protocol == 'TCP' and x.tcp_flags and 'SYN' in x.tcp_flags and 'ACK' not in x.tcp_flags for x in e))"
```

A valid TCP SYN-scan capture should produce TCP events with destination ports and `SYN` flags, allowing `NET-RECON-001` to evaluate the traffic.

## Evidence interpretation

NetDefender findings represent a deterministic match against the documented rule conditions. A `NET-RECON-001` finding indicates that the observed event set matched the TCP SYN reconnaissance threshold; it is not, by itself, proof of compromise or malicious intent. The controlled VMware lab provides the authorized environment for demonstrating the behavior.
