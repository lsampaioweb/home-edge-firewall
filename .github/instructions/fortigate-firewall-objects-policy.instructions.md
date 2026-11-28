---
description: "Use when changing FortiGate address objects, service objects, firewall policies, central SNAT, or DoS policies. Covers object references and permission impact."
applyTo: "ansible/backup/*/firewall_address/*.json,ansible/backup/*/services/**/*.json,ansible/backup/*/firewall_policy/*.json,ansible/backup/*/firewall_central_snat/*.json,ansible/backup/*/firewall_dos_policy/*.json"
---

# FortiGate Firewall Objects And Policies

## Establish The Baseline

- Identify the target VDOM and configuration type, then read the current definition and comparable peer configurations.
- Search the target VDOM's minimal JSON definitions for references to every object being renamed or removed.
- Compare relevant documentation with current minimal JSON. Report conflicts and do not silently copy stale documented values.
- For VLAN-related address or policy changes, also read the [VLAN configuration contract](fortigate-vlan.instructions.md).

## Check Object References

- Before adding or changing a firewall address, verify its name, address type, subnet or range, and associated interface or zone against the requested behavior.
- Before removing or renaming an address or service object, locate references in firewall policies, central SNAT, DoS policies, and service groups as applicable.
- For service groups, verify each member exists and that protocol and port definitions match the requested service.
- Do not require every policy reference to have a custom JSON definition. FortiOS built-in services and interface-derived address objects may be device-provided; verify those against the captured configuration or FortiOS behavior instead of creating duplicate custom objects.
- When a new host address is requested, add a DNS record only if DNS behavior is also requested or required by established configuration evidence.

## Check Policy Impact

- Prefer separate policies per workload or subnet when independent traffic inspection or service restrictions are needed.
- For firewall policy changes, verify source and destination interfaces, address objects, service objects, schedule, action, and policy ID against existing definitions.
- Check policy order and overlapping rules for shadowing. Verify whether the importer preserves the required placement, and report when it does not.
- For central SNAT and DoS policy changes, verify referenced interfaces or zones, addresses, services, and policy IDs.
- Do not infer or add application access, widen address or service scope, or extend per-VLAN permissions unless explicitly requested.
- Adding an interface, zone member, address object, or service object does not by itself authorize changing firewall policies.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify all references resolve and that names and IDs do not conflict within the target VDOM.
- Verify the current import playbook and inventory, then syntax-check affected playbooks. Do not execute live imports unless requested.
- State configuration validation separately from live traffic testing.
