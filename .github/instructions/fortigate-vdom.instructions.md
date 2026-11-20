---
description: "Use when adding or changing FortiGate VDOM definitions. Covers VDOM-scoped configuration, inventory selection, and the current create-only automation boundary."
applyTo: "ansible/backup/system_vdom/*.json"
---

# FortiGate VDOMs

## Establish The Baseline

- Read the system-VDOM definition, current inventory and VDOM variables, VDOM playbooks, and target-VDOM configuration directories before proposing a change.
- Treat `ansible/backup/system_vdom/` as the system VDOM definition area. Treat `ansible/backup/<vdom>/` as the configuration area for that VDOM.
- Verify that the requested VDOM name and short name do not conflict with existing definitions or inventory selection.

## Check Lifecycle Support

- Before creating a VDOM, identify which interface, zone, routing, DNS, DHCP, policy, and management configurations must be placed under its VDOM directory.
- The current system-VDOM role has a create-from-minimal path and no delete task. Do not claim that a VDOM can be safely removed by deleting or editing its JSON; identify the unsupported lifecycle step and request direction.
- Do not move or duplicate existing VDOM configuration unless explicitly requested.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify VDOM names, inventory targeting, configuration directory placement, and available role support.
- Verify the current VDOM import playbook and inventory, then syntax-check it. Do not execute live imports unless requested.
- State configuration validation separately from live VDOM or traffic testing.
