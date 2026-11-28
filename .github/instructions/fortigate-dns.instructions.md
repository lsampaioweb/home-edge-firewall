---
description: "Use when adding, changing, or removing FortiGate DNS database records or DNS service on interfaces. Distinguishes authoritative records from recursive interface service."
applyTo: "ansible/backup/*/dns/*.json,ansible/backup/*/dns_server/*.json"
---

# FortiGate DNS

## Distinguish The Configuration Types

- Treat `dns/*.json` as DNS database and zone records. Treat `dns_server/*.json` as DNS service settings on interfaces; do not substitute one for the other.
- Identify the target VDOM, zone, and interface, then read the current JSON and relevant documentation. Report conflicts rather than silently copying stale documented values.
- For VLAN-related DNS changes, also read the [VLAN configuration contract](fortigate-vlan.instructions.md).

## DNS Database Records

- Keep records in the existing zone definition and allocate IDs without duplicating IDs in that zone.
- When a request adds a new DNS zone rather than a record, inspect the zone type, authoritative behavior, and current DNS playbook support before creating a definition.
- Check record type-specific fields: A and PTR records use IP addresses, while CNAME records reference a canonical name.
- Verify referenced names and addresses against the user's request and current configuration. Add paired A/PTR records only when requested or established by the existing zone convention; do not invent hostnames or addresses.
- When adding or changing a host A or PTR record, check target-VDOM DHCP scopes for an overlapping pool or reservation, including the reserved client's MAC.
- For a host address in a DHCP pool, confirm whether the host uses DHCP. If it does, obtain and verify its MAC and align its reservation; do not invent a MAC or reassign another client's reservation without confirmation.
- When adding or changing a VM host record with a confirmed MAC address, check for a matching MAC-type firewall address object. If one is absent, create it using the confirmed name, MAC, and associated zone; do not alter firewall permissions.
- When changing or removing a record, search the same zone for CNAME references to it.
- Search other target-VDOM JSON for FQDN consumers such as Syslog servers, LDAP servers, and the admin certificate name. A hostname absent from a local zone may be supplied by another DNS source; report unresolved ownership instead of assuming it is invalid or creating a record automatically.

## Interface DNS Service

- Verify each service entry references an existing interface and preserves its intended DNS mode and options.
- When a DHCP scope uses `dns-service: local`, verify that the matching interface has the intended DNS service configuration. Do not assume every interface DNS service requires a DHCP scope.
- Do not add firewall permissions or alter DHCP settings unless the request requires that behavior.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify record IDs and references, or interface names and DNS modes, as applicable.
- Verify every changed FQDN consumer against the intended DNS zone or other documented resolver source.
- Verify the current import playbook and inventory, then syntax-check affected playbooks. Do not execute live imports unless requested.
- State configuration validation separately from live DNS resolution tests.
