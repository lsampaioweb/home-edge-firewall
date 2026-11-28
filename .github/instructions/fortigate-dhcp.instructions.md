---
description: "Use when adding, changing, or removing FortiGate DHCP scopes. Covers interface, subnet, lease, DNS, NTP, and reservation dependencies."
applyTo: "ansible/backup/*/dhcp/*.json"
---

# FortiGate DHCP

## Establish The Baseline

- Identify the target VDOM and exact interface for the scope.
- Read the matching interface definition and comparable DHCP scopes in the same VDOM.
- Compare relevant documentation with current minimal JSON. Report conflicts and do not silently copy stale documented values.
- For a VLAN DHCP change, also read the [VLAN configuration contract](fortigate-vlan.instructions.md); it owns the VLAN dependency checklist.

## Check Scope Dependencies

- Verify that the referenced interface exists and that the DHCP gateway and netmask agree with its configured address.
- Verify that every lease range is inside the subnet and excludes the network, broadcast, and gateway addresses.
- Check scope ID uniqueness, lease-range overlap, reserved-address conflicts, and all existing members before editing a scope.
- Treat `reserved-address` entries as IP-to-client bindings, commonly keyed by MAC. Match each reserved `ip` against the dynamic pool and inspect its binding fields; the absence of a hostname does not mean the address is unreserved.
- When changing a reservation's MAC, check matching MAC-type firewall address objects and their consumers; confirm intended changes before updating them.
- Search other target-VDOM JSON for fixed IP references that fall inside a proposed DHCP pool, including DNS A/PTR records, SNMP notification hosts, Syslog source addresses, and address objects. Require an explicit reservation or a non-overlapping pool when the host assignment is meant to be stable; do not invent reservations.
- When `dns-service` is `local`, verify that the interface has the intended DNS service configuration. DNS database entries under `dns/` are separate from interface DNS service under `dns_server/`.
- When `ntp-service` is `local`, verify that the enabled NTP server configuration includes the exact interface. When it is `specify`, require explicit usable server addresses.
- Treat DNS and NTP settings as separate dependencies. Do not create host records, reservations, or service memberships without the requested data and behavior.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify interface, gateway, subnet, lease-range, DNS, and NTP references against current target-VDOM configuration.
- Verify fixed IP references do not conflict with dynamic lease ranges or DHCP reservations.
- Verify the DHCP minimal backup filter retains every field being changed.
- Verify the current DHCP import playbook and inventory, then syntax-check the affected playbook. Do not execute live imports unless requested.
- State configuration validation separately from live DHCP, DNS, and NTP tests.
