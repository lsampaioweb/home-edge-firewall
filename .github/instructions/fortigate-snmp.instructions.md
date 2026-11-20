---
description: "Use when changing FortiGate SNMP users, queries, traps, or notification targets. Covers interface reachability, DHCP pool conflicts, and secret handling."
applyTo: "ansible/backup/*/snmp/*.json"
---

# FortiGate SNMP

## Establish The Baseline

- Read the target VDOM's SNMP user JSON, paired capture, documentation, and the role's minimal-key filter and importer.
- Distinguish SNMP query access, trap status, notification hosts, event selection, and firewall-wide SNMP agent settings. Do not infer one from another.
- Check whether the requested agent setting is represented by a minimal JSON area; do not invent an SNMP agent JSON file when the project only manages the user entry.

## Check Notification And Secret Dependencies

- Verify notification host IPs are assigned to the intended monitoring hosts and do not fall inside DHCP dynamic ranges unless reserved or otherwise explicitly intended.
- Verify SNMP source IPs match the intended interface and check the corresponding address, route, and access-policy references when relevant.
- SNMP authentication and privacy passwords come from Ansible's secret lookup, not the minimal JSON. Never add, print, or request those secrets in chat.
- Do not enable traps, queries, events, or access permissions unless requested.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify notification hosts, interface addresses, status fields, and importer field mappings.
- Verify the current SNMP import playbook and inventory, then syntax-check it. Do not execute live imports unless requested.
- State configuration validation separately from live polling or trap-delivery tests.
