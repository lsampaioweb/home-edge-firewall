---
description: "Use when adding, importing, or updating FortiGate VLANs in this project. Covers dependent DHCP, DNS service, NTP, zone membership, subnet objects, validation, and minimal JSON import commands; keeps policy permissions separate."
applyTo: "ansible/backup/*/system_interface/vlan/*.json,ansible/backup/*/dhcp/*.json,ansible/backup/*/dns_server/*.json,ansible/backup/*/ntp/*.json,ansible/backup/*/system_zone/*.json,ansible/backup/*/firewall_address/*.json"
---

# FortiGate VLAN Configuration

## Establish The Baseline

- Apply the dependency checklist below whenever a request adds or imports VLANs, even if the request names only the interface directory.
- Identify the target VDOM and environment before selecting peer configuration.
- Compare the supplied VLAN catalog with existing VLAN IDs and interface names.
- Read a complete existing peer configuration across all six checklist areas before choosing settings.
- Preserve existing abbreviated interface names when other objects reference them.
- Treat a VLAN catalog as evidence of VLAN identity, not proof of its IP subnet, gateway, or parent interface.
- Follow a consistent addressing and parent-interface pattern in the target environment; ask for missing network details when peer configuration does not establish one.

## Required Dependency Checklist

Paths below are relative to `ansible/backup/<vdom>/`.

| Area | Configuration | Required parity for each new VLAN |
| --- | --- | --- |
| Interface | `system_interface/vlan/<vlan>.json` | VLAN ID, interface name, parent, gateway/netmask, VDOM, and peer interface settings. |
| DHCP | `dhcp/<id>-<vlan>.json` | Unique scope ID, interface reference, gateway, netmask, lease range, DNS service, domain, NTP advertisement, and enabled status. |
| Interface DNS service | `dns_server/<vlan>.json` | Interface name and the peer DNS operating mode. |
| NTP service | `ntp/*.json` | Membership in the existing NTP server interface list when peers receive this service. |
| Zone | `system_zone/*.json` | Membership in the matching environment zone, preserving its existing isolation setting. |
| Subnet address | `firewall_address/<vlan>-subnet.json` | Subnet name, network/netmask, and matching zone association. |

- Complete every checklist row for every new VLAN unless the user explicitly requests an exception or current peer configuration establishes that the service does not apply.
- Preserve all existing members when extending shared zone or NTP interface lists.
- Set DHCP `ntp-service` to `local` for VS and VP VLANs served by the FortiGate NTP server.
- Treat NTP server interface membership and DHCP NTP advertisement as separate requirements.
- Inspect the current peer files instead of treating the following staging example as a permanent global default: `VS-MONITOR` uses VLAN `1155`, parent `SS-S-VMS`, gateway `10.1.55.14/28`, DHCP leases `10.1.55.1` through `10.1.55.13`, local DNS, domain `lan.home`, recursive interface DNS, and zone `zone-staging`.
- Do not copy staging addressing or parent interfaces into the production environment.

## Separate Services From Permissions

- Treat DHCP, interface DNS, and NTP parity as distinct from firewall policy permissions.
- Inspect zone-based firewall, central SNAT, and DoS rules to determine whether zone membership already provides the existing shared coverage.
- Do not copy or extend per-VLAN access policies unless the user requests those permissions.
- Preserve `intrazone` behavior when extending a zone; zone membership must not become an implicit allow-all between VLANs.
- Do not invent application port rules, DHCP reservations, or DNS host records without the corresponding requirements or host data.
- Do not duplicate single-purpose settings such as the monitoring VLAN's syslog source address for every new VLAN.

## Preserve The Backup Contract

- Author desired configuration in minimal `.json` files consumed by the `create-from-minimal` playbooks.
- Treat `.bkp` files as captured device configuration consumed by the `create-from-backup` playbooks; do not fabricate raw backups or device-assigned metadata.
- Keep runtime playbook or role changes out of a VLAN data update unless the existing loader or backup filter cannot preserve the required configuration.
- Backup playbooks regenerate both formats from device data; follow the [project backup safeguard](../copilot-instructions.md).

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Check for duplicate VLAN IDs on a parent interface, duplicate interface names, duplicate DHCP scope IDs, and overlapping subnets within the target VDOM.
- Verify that DHCP, DNS service, zone membership, and NTP membership reference the exact interface name.
- Verify that DHCP `ntp-service: local` has a matching interface in the enabled NTP server's interface list.
- Require usable explicit server addresses when DHCP `ntp-service` is `specify`.
- Verify that the DHCP minimal backup filter retains `ntp-service` and `ntp-server1` through `ntp-server3`.
- Verify that each DHCP gateway matches its interface IP and that lease endpoints lie in the subnet without including the gateway, network address, or broadcast address.
- Verify that each subnet address object matches its VLAN network and zone.
- Compare shared lists before and after the edit to confirm that existing members and isolation settings are preserved.
- Search the target VDOM's other JSON for references to the VLAN interface IP or stable host IPs in its subnet, including DNS A/PTR records, Syslog `source-ip`, SNMP notification hosts, and DHCP reservations. Keep such references aligned when the requested address changes; do not replicate monitoring settings to unrelated VLANs.
- Run `ansible-playbook --syntax-check` for the affected import playbooks using the maintained inventory.
- Compare captured configuration with preserved pre-import definitions; agreement between regenerated minimal and full backups alone does not prove that intended settings were applied.
- Distinguish configuration validation from live DHCP, DNS, NTP, and connectivity tests; report live behavior as unverified unless tested.

## Provide The Import Commands

Commands run from `ansible/`; the maintained inventory is `inventory/hosts`.

| Changed area | Import playbook |
| --- | --- |
| VLAN interfaces | `07-system-interface-create-from-minimal.yml` |
| Interface DNS service | `09-dns-server-create-from-minimal.yml` |
| NTP service | `10-ntp-create-from-minimal.yml` |
| Zone membership | `12-system-zone-create-from-minimal.yml` |
| DHCP scopes | `13-dhcp-create-from-minimal.yml` |
| Subnet addresses | `17-firewall-address-create-from-minimal.yml` |

- Verify the current playbook names and inventory before supplying executable commands.
- Provide full commands for every changed area in dependency order: interfaces first, zones before zone-associated address objects, and DNS service before DHCP with local DNS.
- State that each import processes all matching saved definitions for its configuration area, not only the newly added VLANs.
- Do not execute live imports unless the user asks for execution.
- In the completion report, account for all six checklist areas and explain any exceptions; identify policy permissions left unchanged separately.
