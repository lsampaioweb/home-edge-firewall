# Home Edge Firewall Ansible Project

## Project Overview
This is an Ansible automation project for managing a Fortigate firewall configuration.
The project follows a modular approach with roles, playbooks, and supports both full backup/restore and minimal JSON-based configuration.

## Technology Stack
- **Primary**: Ansible with fortinet.fortios collection.
- **Target Platform**: Fortigate firewall via HTTPAPI.
- **Development Environment**: macOS/Ubuntu with pipx-managed Ansible.
- **Version Control**: Git/GitHub.

## Architecture Principles

### Three-Tier Approach
Each Fortigate feature has three numbered playbooks and matching task files:
1. `XX-feature-backup.yml` / `backup.yml` — Exports current config to `.bkp` and `.json` files.
2. `XX-feature-create-from-backup.yml` / `create-from-backup.yml` — Restores from full `.bkp` backup.
3. `XX-feature-create-from-minimal.yml` / `create-from-minimal.yml` — Creates from minimal `.json`.

### Data Management
- **Full backups**: `.bkp` files with all Fortigate parameters.
- **Minimal configs**: `.json` files with only UI-visible parameters.
- Organized by feature in `backup/root/` directory structure.

## Code Style & Conventions

### Playbook Template
```yaml
---
- name: "Descriptive action with feature name"
  hosts: "firewalls"
  gather_facts: false  # ALWAYS false for Fortigate.

  tasks:
    - name: "Action description"
      ansible.builtin.include_tasks: "{{ path_role_feature }}/task-file.yml"
```

### Task File Template
```yaml
---
- name: "Reading the json file '{{ file.path }}' that contains the desired settings"
  ansible.builtin.set_fact:
    desired_settings: "{{ lookup('file', file.path) | from_json }}"

- name: "Printing the desired settings json object"
  ansible.builtin.debug:
    msg: "{{ desired_settings }}"
  tags: ["never", "debug"]

- name: "Creating/Updating [Feature] entry: {{ desired_settings.name }}"
  fortinet.fortios.fortios_[module_name]:
    vdom: "{{ vdom | default(omit, true) }}"
    state: "present"
    [module_config]:
      name: "{{ desired_settings.name }}"
      required_field: "{{ desired_settings.required_field }}"
      optional_field: "{{ desired_settings.optional_field | default(omit, true) }}"
      # Hyphenated JSON keys must use bracket notation:
      hyphenated_field: "{{ desired_settings['hyphenated-param'] | default(omit, true) }}"
  register: "output"

- name: "Debug"
  ansible.builtin.debug:
    msg: "{{ output }}"
  tags: ["never", "debug"]
```

### Variable Naming
- Use descriptive names with underscores: `desired_settings`, `backup_files`.
- Prefix path variables: `path_role_`, `path_backup_`.

## File Organization

### Directory Structure
```
playbook/
├── [01-99]-*.yml                    # Individual feature playbooks
├── site-*.yml                       # Master playbooks
├── ansible.cfg
├── roles/
│   └── [feature]/
│       ├── tasks/
│       │   ├── backup.yml
│       │   ├── create-from-backup.yml
│       │   ├── create-from-minimal.yml
│       │   └── add-entry*.yml
│       └── vars/
│           └── main.yml             # <role>_minimal_keys defined here
├── backup/root/
│   └── [feature]/
│       ├── *.bkp                    # Full backup files
│       └── *.json                   # Minimal config files
└── inventory/
    └── hosts
```

### Naming Conventions
- **Playbooks**: `##-feature-action.yml` (zero-padded numbers).
- **Backup/minimal files**: `lowercase-name.bkp` / `lowercase-name.json` (matching filenames).
- **DHCP/numbered files**: `%04d-<interface-lowercase>.json` (4-digit ID matching VLAN ID).

## Network Configuration Standards

### VLAN Scheme
- **Staging**: VLAN IDs 1110–1180, IP range 10.1.X.X/28. Interfaces: `VS-*`, software switch `SS-S-VMS` / `SS-S-CLSTR`, zone `zone-staging`.
- **Production**: VLAN IDs 2110–2180, IP range 20.1.X.X/28. Interfaces: `VP-*`, software switch `SS-P-VMS` / `SS-P-CLSTR`, zone `zone-production`.
- VLAN ID maps to third octet via last two digits: VLAN 1110 → 10.1.10.0/28, VLAN 2135 → 20.1.35.0/28.
- Standard /28 subnets: .0 = network, .1–.13 = DHCP range, .14 = gateway, .15 = broadcast.

### Interface Name Truncation
FortiGate enforces a 15-character interface name limit. Always use the exact shortened name in any file that references these interfaces:
| Full name | FortiGate name |
|-----------|----------------|
| VS-REPOSITORY | VS-REPOSITR |
| VS-JUMPSERVER | VS-JUMPSRV |
| VS-LOADBALANCER | VS-LDBLANCER |
| VP-REPOSITORY | VP-REPOSITR |
| VP-JUMPSERVER | VP-JUMPSRV |
| VP-LOADBALANCER | VP-LDBLANCER |

## Firewall Management Access

### Interface allowaccess Policy
Management access (HTTPS/SSH) is controlled exclusively by `allowaccess` on each interface — **not** by firewall policies (which only govern through-traffic). The rule is:

| Interface | allowaccess | Audience |
|-----------|-------------|----------|
| LAG-Home | `ping https ssh fabric` | Home machine (192.168.3.x) |
| VS-MGMT | `ping https ssh fabric` | Staging management VMs |
| VP-MGMT | `ping https ssh fabric` | Production management VMs |
| INT-loopback | `ping snmp fabric` | NTP/SNMP services only — never HTTPS/SSH |
| All other VLANs | `ping` or nothing | No management access |

### DNS Naming Convention for Firewall Management
Each audience uses a distinct hostname pointing to their local gateway IP:

| Zone | Hostname | IP | Users |
|------|----------|----|-------|
| `lan.home` | `firewall-01.lan.home` | `192.168.3.1` | Home machine |
| `lan.homelab` | `firewall-01-stg.lan.homelab` | `10.1.10.14` | Staging mgmt VMs |
| `lan.homelab` | `firewall-01-prd.lan.homelab` | `20.1.10.14` | Production mgmt machines |

### PTR Record Rules
- FortiGate enforces **one PTR per IP** across all zones — attempting a second PTR for the same IP in any zone returns error `-6054`.
- Keep one PTR per unique IP in the zone that owns that IP range.
- Never add a PTR in `lan.homelab` for an IP that already has a PTR in `lan.home`.

## AI Assistant Instructions

1. **NEVER** use pip commands — only pipx or homebrew.
2. When creating new features, copy patterns from existing roles like `dns` or `dhcp` rather than inventing new approaches.
3. **NEVER** truncate command output — do not append `| tail`, `| head`, `| grep` or any other filter to playbook or terminal commands. Always show the full output.
4. **Always read files before assuming their content** — never modify or advise based on assumed state.

## Role Checklist (apply to every role when reviewing or fixing)

When working on any role, always go through these steps in order:

1. **`gather_facts: false`** — Verify all 3 playbooks have `gather_facts: false`.
2. **Minimal fields** — Check the existing hand-crafted `.json` files in `backup/root/<role>/` to determine the correct minimal keys. The union of all keys across all files is the baseline.
3. **`vars/main.yml`** — Verify the file exists in `roles/<role>/vars/main.yml` with the `<role>_minimal_keys` list. Without it, the backup silently skips saving `.json` files.
4. **`backup.yml`** — Verify it uses `path_common_firewall_save_backup_files` with `minimal_keys` set, and applies `remove_keys` for `invalid_attribute`. For hyphenated keys, follow the rules below.
5. **Hyphenated key strategy** — Two rules, applied per key:
   - **Top-level keys** (e.g. `source-ip`, `lease-time`): do NOT rename in `backup.yml`. Keep the hyphenated key in `.bkp`/`.json` files. In `add-entry.yml`, read with bracket notation: `desired_settings['source-ip']`. In `vars/main.yml` minimal_keys list, use the hyphenated name.
   - **Sub-keys inside nested lists** (e.g. `start-ip` inside each element of an `ip-range` list): DO rename using `replace_keys` in `backup.yml`. In `add-entry.yml`, read with dot notation (the whole list is passed as-is, sub-keys are already underscored).
   - To decide which rule applies: inspect the raw FortiGate data (from a `.bkp` file or debug output) and check whether the hyphenated key is at the top level of the entry dict or nested inside a list of sub-dicts.
   - **Name collision** — When the same hyphenated key name exists at BOTH the top level AND inside a nested list (e.g. `lease-time` is a top-level DHCP key AND a sub-key inside each `ip-range` item), the main `replace_keys` pipeline must NOT rename it (top-level rule applies). Instead, use `combine({'<nested-key>': item['<nested-key>'] | ... | replace_keys(...)})` to apply renaming only to the sub-dicts in isolation — the same pattern used for `ipv6` in `system_interface/tasks/backup-by-type.yml`. In `vars/main.yml`, the `nested_minimal_keys` list must use the **underscored** name (e.g. `lease_time`) since the sub-dicts have already been renamed by the time `save_backup_files` filters them.
6. **Nested list key filtering** — When a top-level key holds a list of sub-dicts that need their own minimal-key pruning (e.g. `ip-range`, `dns-entry`), pass two extra vars to `path_common_firewall_save_backup_files`:
   - `nested_key: "<key-name>"` — the top-level key whose list of sub-dicts should be filtered.
   - `nested_minimal_keys: "{{ <role>_<nested>_minimal_keys }}"` — list of sub-dict keys to keep (defined in `vars/main.yml`).
   The `save_backup_files` common task handles the filtering natively. See the `dns` role (`nested_key: "dns-entry"`) and `dhcp` role (`nested_key: "ip-range"`) for reference.
7. **`create-from-backup.yml` and `create-from-minimal.yml`** — Verify they use `path_common_firewall_get_backup_files`, loop with `loop_var: file`, and call `add-entry.yml`:
   ```yaml
   - name: "Retrieving the [type] files"
     ansible.builtin.include_tasks: "{{ path_common_firewall_get_backup_files }}"
     vars:
       paths: "{{ backup_feature_path }}"
       patterns: "{{ backup_files_extension }}"  # or minimal_files_extension

   - name: "Creating [Feature] entries"
     ansible.builtin.include_tasks: "add-entry.yml"
     loop: "{{ backup_files.files | default([]) | sort(attribute='path') }}"
     loop_control:
       loop_var: "file"
       label: "{{ file.path }}"
   ```
8. **`add-entry.yml` — space-separated fields** — Check for fields that the FortiGate API returns as a space-separated string but the module expects as a list (e.g. `allowaccess`). Fix with `.split(' ') | select() | list`.
9. **`add-entry.yml` — missing fields** — Cross-check fields against the module's `.keys` files (if present) and the `.bkp` files to ensure no important parameters are omitted.
10. **Run all 3 playbooks** — Use full output (no `tail`/`grep` truncation) so failures are visible. Run backup first, then create-from-minimal, then create-from-backup.
11. **API limitations** — Note any resources the FortiGate API cannot create programmatically (e.g. loopback interfaces require manual UI/CLI creation first).
12. **Site playbooks** — After creating or deleting a role, update all three site playbooks (`site-backup.yml`, `site-create-from-backup.yml`, `site-create-from-minimal.yml`) to add or remove the corresponding `import_playbook` entries in numbered order.
13. **README** — After creating or deleting a role, add or remove the corresponding numbered section in `playbook/README.md`, keeping entries in numbered order.
14. **Documentation** — After creating or deleting a role, create or remove the matching `.txt` file(s) under `documentation/01-Config/` in the appropriate FortiGate UI section folder. The file must document the actual configured values using the same free-form structured text style as existing files.
