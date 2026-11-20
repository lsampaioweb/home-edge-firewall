---
description: "Use when changing FortiGate static routes or SD-WAN configuration. Covers WAN interface members, gateways, zones, routes, and policy references."
applyTo: "ansible/backup/*/static_routing/*.json,ansible/backup/*/system_sdwan/*.json"
---

# FortiGate Routing And SD-WAN

## Establish The Baseline

- Identify the target VDOM and read the current route or SD-WAN configuration, WAN interfaces, and comparable peers.
- Compare relevant documentation with current minimal JSON. Report conflicts and do not silently copy stale documented values.
- Search policies and other routes for references to an affected interface or SD-WAN zone before renaming or removing it.

## Check Related Configuration

- For a static route, verify the destination, gateway, distance, priority, status, and outgoing interface or SD-WAN zone against current configuration and requested traffic path.
- For an SD-WAN member, verify the referenced WAN interface and gateway. Check routes and firewall policies that use the affected SD-WAN zone.
- When changing a WAN interface or its addressing, inspect SD-WAN membership and static routes that rely on it.
- Do not change firewall policy permissions or traffic steering beyond the requested route or SD-WAN behavior.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify interface, gateway, zone, route, and policy references resolve in the target VDOM.
- Verify the current import playbook and inventory, then syntax-check affected playbooks. Do not execute live imports unless requested.
- State configuration validation separately from live reachability and failover tests.
