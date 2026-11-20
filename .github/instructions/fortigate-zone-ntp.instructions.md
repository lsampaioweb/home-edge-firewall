---
description: "Use when changing FortiGate interface zones or NTP service membership. Covers interface references, zone isolation, DHCP NTP settings, and consumers of zone names."
applyTo: "ansible/backup/*/system_zone/*.json,ansible/backup/*/ntp/*.json"
---

# FortiGate Zones And NTP

## Establish The Baseline

- Identify the target VDOM and read the complete current zone or NTP definition, including all existing members.
- Compare relevant documentation with current minimal JSON. Report conflicts and do not silently copy stale documented values.
- For VLAN-related changes, also read the [VLAN configuration contract](fortigate-vlan.instructions.md).

## Zone Membership

- Verify every added member is an existing interface in the target VDOM.
- Preserve existing members and the zone's `intrazone` setting when extending a zone.
- Before renaming or removing a zone, search firewall policies, central SNAT, DoS policies, and address objects for references to that zone.
- Treat membership as interface grouping, not permission to communicate. Do not broaden firewall policies or intrazone behavior unless explicitly requested.

## NTP Service

- When changing the NTP server interface list, preserve existing members and verify each interface exists in the target VDOM.
- Search DHCP definitions for `ntp-service: local` scopes that reference affected interfaces. Check `ntp-service: specify` scopes for usable explicit server addresses.
- Keep NTP server interface membership separate from DHCP NTP advertisement; validate both when both are in scope.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify exact interface and zone references, preserved members, and unchanged isolation settings unless requested.
- Verify the current import playbook and inventory, then syntax-check affected playbooks. Do not execute live imports unless requested.
- State configuration validation separately from live zone traffic or NTP tests.
