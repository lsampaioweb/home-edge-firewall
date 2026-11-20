---
description: "Use when changing FortiGate LDAP server configuration. Covers directory endpoint and identity fields, remote-group/admin references, DNS dependencies, and the importer password boundary."
applyTo: "ansible/backup/*/ldap/*.json"
---

# FortiGate LDAP

## Establish The Baseline

- Identify the target VDOM and read its LDAP JSON, paired capture, and matching LDAP documentation.
- Compare the server name, port, secure mode, base DN, common-name identifier, and bind username across those sources. Report conflicts rather than silently copying stale documentation.
- Resolve the configured server name against its intended DNS source. Do not create a DNS record unless requested and supported by the zone configuration.

## Check Consumers And Secret Handling

- Before renaming or removing an LDAP server, inspect the documented user-group and administrator configuration for references to its object name and remote-group names.
- User groups and administrator entries have no minimal-JSON importer in this project. Do not invent JSON files or claim those settings are managed by the LDAP role.
- The LDAP add-entry task does not pass a bind password. Do not claim that a password change is applied by editing the JSON; inspect supported secret handling and ask before proposing an unsupported runtime change.
- Do not expose credentials in JSON, logs, or command output.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify the LDAP object name, endpoint, port, secure mode, and referenced directory identities.
- Verify the current LDAP import playbook and inventory, then syntax-check it. Do not execute live imports unless requested.
- State configuration validation separately from live bind and group-membership tests.
