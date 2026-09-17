# Real PCAP Analysis

NetDefender analyzes PCAP/PCAPNG captures through the TShark adapter in `netdefender/capture.py`.

## TShark Fields

The adapter extracts:

- `frame.time_epoch` — packet timestamp;
- `ip.src` — source IPv4 address;
- `ip.dst` — destination IPv4 address;
- `ip.proto` — numeric IP protocol identifier;
- `tcp.srcport` — TCP source port when present;
- `tcp.dstport` — TCP destination port when present;
- `udp.srcport` — UDP source port when present;
- `udp.dstport` — UDP destination port when present;
- `tcp.flags` — numeric TCP flag bitmask when present;
- `frame.len` — packet length.

The adapter uses a tab separator so comma-separated address fields do not corrupt the extracted columns.

## Protocol Normalization

The adapter maps:

| IP protocol | NetDefender protocol |
|---:|---|
| `1` | `ICMP` |
| `6` | `TCP` |
| `17` | `UDP` |

Known protocol names are preserved. Other non-empty values are normalized to uppercase. Missing values become `UNKNOWN`.

## TCP Flag Normalization

TShark may return TCP flags as a numeric bitmask. NetDefender converts the bitmask into stable names.

Examples:

- `0x0002` → `SYN`
- `0x0012` → `SYN,ACK`

This allows the TCP detection rule to distinguish SYN probes from SYN/ACK responses.

## IP Normalization

TShark can produce comma-separated address fields in some capture contexts. NetDefender normalizes such values by using the final address in the field.

For example:

```text
172.16.198.128,172.16.198.129
        ↓
172.16.198.129
```

The behavior is covered by a regression test because incorrect column/address handling can create false detector groups.

## Transport-Port Extraction

The adapter extracts both TCP and UDP source/destination ports. For each normalized event, the populated transport port is selected for the corresponding source or destination field.

This is necessary because UDP reconnaissance does not contain TCP port fields.

## Controlled Lab Workflow

```text
Kali
  ↓
Nmap
  ↓
Metasploitable
  ↓
Wireshark / TShark
  ↓
PCAP/PCAPNG
  ↓
NetDefender TShark adapter
  ↓
NetworkEvent objects
  ↓
Detection engine
  ↓
JSON / HTML findings
```

For final evidence, an unfiltered capture is preferable because it preserves the complete packet context. Wireshark display filters change what is displayed; they do not retroactively define what was written to the capture file.

## Real Capture Commands

TCP example:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/tcp-syn-scan-001.pcapng
```

UDP example:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/udp-scan-001.pcapng
```

Control example:

```bash
python -m netdefender.cli /home/kali/NetDefender-evidence/tcp-control-001.pcapng
```

Generate HTML:

```bash
python -m netdefender.cli /path/to/capture.pcapng --html report.html
```

## Evidence Interpretation

A `NET-RECON-001` finding means the observed TCP events matched the documented TCP threshold.

A `NET-RECON-002` finding means the observed UDP events matched the documented UDP threshold.

An empty result `[]` means none of the currently enabled rules matched the supplied evidence.

These results are deterministic classifications of the supplied event data. They are not proof of compromise or malicious intent.
