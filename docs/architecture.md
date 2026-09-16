# NetDefender Architecture

## Purpose

NetDefender is a controlled enterprise-network security lab. The architecture is designed to demonstrate how segmentation, firewall policy, intrusion detection, VPN access, TLS, and cryptographic controls work together rather than as isolated technologies.

## MVP Architecture

```text
                         Untrusted Network
                                |
                                |
                           +----------+
                           |  pfSense |
                           | Firewall |
                           +----+-----+
                              / | \
                             /  |  \
                           DMZ Internal VPN
                            |      |     |
                            |      |     |
                       DMZ Server Internal VPN Client
                                  Client

                         +----------------+
                         |    Snort IDS   |
                         +--------+-------+
                                  |
                             Monitoring
```

The final implementation may place Snort at a more precise observation point depending on the VirtualBox interface design. The diagram will be updated as the lab is implemented and verified.

## Security Flow

```text
Build Network
     ↓
Run Controlled Test
     ↓
Capture Traffic
     ↓
Detect Activity
     ↓
Enforce Policy
     ↓
Review Evidence
```

## Trust Zones

### Untrusted

The controlled testing side of the lab. Kali Linux will generate authorized reconnaissance and security-test traffic.

### DMZ

The simulated enterprise's externally reachable service zone. Services placed here will be intentionally limited so firewall and IDS behavior can be demonstrated clearly.

### Internal

The trusted enterprise zone. Access from less-trusted zones will be restricted by explicit firewall policy.

### VPN

The remote-access zone used to demonstrate authenticated, encrypted access to selected internal resources through OpenVPN.

## Phase Plan

1. **Topology and connectivity** — create the isolated VirtualBox network and verify interfaces and reachability.
2. **Firewall and segmentation** — configure pfSense interfaces and explicit inter-zone policy.
3. **DMZ services** — deploy a small controlled service target for testing.
4. **IDS** — deploy Snort and validate selected detection rules.
5. **Reconnaissance and packet evidence** — use Kali/Nmap and Wireshark to generate and document controlled traffic.
6. **TLS/HTTPS** — create certificates with OpenSSL and compare HTTP and HTTPS captures.
7. **VPN** — configure OpenVPN and demonstrate restricted remote access.
8. **Cryptography** — demonstrate hashing, HMAC, public-key cryptography, and digital signatures in focused scenarios.
9. **Integration and validation** — run repeatable end-to-end scenarios and collect evidence.
10. **Final documentation** — synchronize README, architecture/setup/testing documentation, evidence, report, and presentation with the implemented MVP.

## Design Principles

- Keep the environment isolated and controlled.
- Use least-privilege firewall rules.
- Prefer small, repeatable demonstrations over large infrastructure.
- Keep security evidence tied to an observable test result.
- Do not claim a control works without validating it in the lab.
- Keep configuration and documentation synchronized with the implementation.
