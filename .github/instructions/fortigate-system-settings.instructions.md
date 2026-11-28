---
description: "Use when changing FortiGate global system settings. Covers administrator access, hostname, certificate references, NTP ownership, and importer field support."
applyTo: "ansible/backup/*/system_settings/*.json"
---

# FortiGate System Settings

## Establish The Baseline

- Read the system-settings JSON selected by the current backup context, its paired capture, relevant documentation, and the role's minimal-key filter and importer.
- Treat `system_settings` as FortiGate-wide settings. Verify how the role targets the firewall; do not infer VDOM scope from the JSON directory alone.
- Compare the admin certificate name and administrator ports with current configuration and relevant certificate workflow before editing.

## Check Related Configuration

- Before changing `admin-server-cert`, verify that the named certificate exists in the captured configuration and matches the certificate upload workflow. Certificate material is handled by the certificate role, not a minimal JSON area.
- Before changing hostname or administrator access ports, check dependent DNS names, inventory access, HTTPS redirect, and current management reachability. Do not risk locking out the maintained Ansible connection.
- FortiGate NTP server mode and interface membership are managed separately under `ntp/`; read the [zone and NTP contract](fortigate-zone-ntp.instructions.md) for those changes.
- Verify importer support separately from minimal-backup retention: fields mapped by the importer may still be omitted when a backup regenerates the JSON.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify certificate names, access settings, DNS dependencies, and supported fields against current target-VDOM configuration.
- Verify the current system-settings import playbook and inventory, then syntax-check it. Do not execute live imports unless requested.
- State configuration validation separately from live administrator access or certificate-chain testing.
