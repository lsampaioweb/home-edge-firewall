---
description: "Use when adding, changing, or removing FortiGate interfaces. Covers interface types, parent-child relationships, and configuration references that may need coordinated updates."
applyTo: "ansible/backup/*/system_interface/**/*.json"
---

# FortiGate Interfaces

## Establish The Baseline

- Identify the target VDOM and interface type before editing.
- Read the current interface definition and comparable peers in the same VDOM.
- For parent-interface changes, find all child VLANs and other configurations that reference the parent before changing or removing it.
- Search the target VDOM's minimal JSON definitions for references to the interface name before renaming or removing it.
- Before changing an interface IP, also search for that literal address in DHCP scopes, DNS records, firewall address objects, Syslog source settings, and SNMP notification or source settings.
- Compare relevant documentation with current minimal JSON. Report conflicts and do not silently copy stale documented values.

## Check Related Configuration

- For VLAN interfaces, read the [VLAN configuration contract](fortigate-vlan.instructions.md). It owns the VLAN dependency checklist and import guidance.
- For other interface changes, inspect DHCP scopes, interface DNS services, NTP server membership, zone membership, static routes, SD-WAN members, firewall policies, central SNAT, DoS policies, and address objects where those configurations reference the interface.
- Treat IP-address references as dependencies even when they do not contain the interface name. Update them only when required by the requested behavior.
- Update only the dependent configurations required by the requested behavior. Do not expand firewall permissions as an incidental interface change.
- Preserve existing interface names when other objects reference them. Do not infer addressing, parent interfaces, or administrative access from a VLAN catalog or a different environment.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Check interface names, parent interfaces, VDOM, and type-specific identifiers against the target VDOM's existing definitions.
- Verify that references to the changed interface still resolve in each affected configuration area.
- Verify the applicable import playbook names and syntax-check affected playbooks; do not execute live imports unless requested.
- State configuration validation separately from live connectivity or service testing.
