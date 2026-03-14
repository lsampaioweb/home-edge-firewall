# Home Edge Firewall Ansible Project

## Project Overview
This is an Ansible automation project for managing a Fortigate firewall configuration.
The project follows a modular approach with roles, playbooks, and supports both full backup/restore and minimal JSON-based configuration.

## Technology Stack
- **Primary**: Ansible with fortinet.fortios collection.
- **Target Platform**: Fortigate firewall via HTTPAPI.
- **Development Environment**: macOS/Ubuntu with pipx-managed Ansible.
- **Version Control**: Git/GitHub.
- **Documentation**: Plain text files and structured directories.

## Architecture Principles

### Playbook Structure
- Each major Fortigate feature has its own numbered playbook (e.g., `07-dns-backup.yml`).
- Three-tier approach per feature:
  1. `XX-feature-backup.yml` - Exports current config.
  1. `XX-feature-create-from-backup.yml` - Restores from full backup.
  1. `XX-feature-create-from-minimal.yml` - Creates from minimal JSON.

### Role-Based Organization
- Each feature has a dedicated role under `roles/`, with task files mirroring the three-tier playbook structure (see Directory Structure).

### Data Management
- **Full backups**: `.bkp` files with all Fortigate parameters.
- **Minimal configs**: `.json` files with only UI-visible parameters.
- Organized by feature in `backup/root/` directory structure.

## Code Style & Conventions

### Playbook Standards
```yaml
---
- name: "Descriptive action with feature name"
  hosts: "firewalls"
  gather_facts: false  # ALWAYS false for Fortigate.

  tasks:
    - name: "Action description"
      ansible.builtin.include_tasks: "{{ path_role_feature }}/task-file.yml"
```

### Task File Patterns
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
```

### Variable Naming
- Use descriptive names with underscores: `desired_settings`, `backup_files`.
- Prefix path variables: `path_role_`, `path_backup_`.
- Use consistent suffixes: `_path`, `_files`, `_extension`.

### Error Handling & Debugging
- Include debug tasks with `tags: ["never", "debug"]`.
- Register outputs as `output` for consistency.
- Use `default(omit, true)` for optional Fortigate parameters.
- Let Fortigate handle validation - don't over-validate in Ansible.

## File Organization Standards

### Directory Structure
```
playbook/
├── [01-99]-*.yml                    # Individual feature playbooks
├── site-*.yml                       # Master playbooks
├── ansible.cfg                      # Ansible configuration
├── roles/
│   └── [feature]/
│       └── tasks/
│           ├── backup.yml
│           ├── create-from-backup.yml
│           ├── create-from-minimal.yml
│           └── add-entry*.yml
├── backup/root/
│   └── [feature]/
│       ├── *.bkp                    # Full backup files
│       ├── *.json                   # Minimal config files
│       ├── custom/                  # For services
│       └── groups/                  # For service groups
└── inventory/
    └── hosts                        # Inventory file
```

### Naming Conventions
- **Playbooks**: `##-feature-action.yml` (zero-padded numbers).
- **Backup files**: `lowercase-name.bkp`.
- **Minimal files**: `lowercase-name.json` (matching .bkp filename).
- **VLAN files**: `###-VL-ENV-ROLE.txt`.

## JSON Structure Standards

### Minimal JSON Requirements
- **Custom Services**: Must include `name`, `category`, `protocol`.
- **Service Groups**: Must include `name`, `member`.
- **DNS**: Must include `name`, `domain`, `type`.
- Only include parameters visible in Fortigate UI.
- Use exact parameter names from corresponding `.bkp` files.

## Network Configuration Standards

### VLAN Scheme
- **Home-Infra**: VLAN IDs 1110–1180, IP range 10.1.X.X/28.
- **Homelab**: VLAN IDs 2110–2180, IP range 20.1.X.X/28.
- VLAN ID maps to third octet via last two digits: VLAN 1110 → 10.1.10.0/28, VLAN 2135 → 20.1.35.0/28.
- Standard /28 subnets: .0 = network, .1–.13 = DHCP range, .14 = gateway, .15 = broadcast.

### Inventory Requirements
```ini
[firewalls:vars]
ansible_user=admin
ansible_network_os=fortinet.fortios.fortios
ansible_connection=httpapi
ansible_httpapi_use_ssl=true
vdom=root
```

## Quality Guidelines

### Idempotency
- All playbooks must be safely re-runnable.
- Use `state: present` for create operations.
- Rely on Fortigate's built-in change detection.

### Testing Approach
- Start with low-risk features (services, DNS) before network changes.
- Use backup playbooks before making changes.
- Test minimal JSON with non-critical elements first.

### Documentation Standards
- Maintain text files in `documentation/` matching UI structure.
- Keep README focused on commands and purpose, not verbose explanations.
- Update `copilot-context.md` for major workflow changes.

## Common Patterns to Follow

### File Processing Loop
```yaml
- name: "Retrieving the [type] files"
  ansible.builtin.include_tasks: "{{ path_common_firewall_get_backup_files }}"
  vars:
    paths: "{{ backup_feature_path }}"
    patterns: "{{ backup_files_extension }}"  # or minimal_files_extension

- name: "Creating [Feature] entries from [type]"
  ansible.builtin.include_tasks: "add-entry.yml"
  loop: "{{ backup_files.files | default([]) | sort(attribute='path') }}"
  loop_control:
    loop_var: "file"
    label: "{{ file.path }}"
```

## AI Assistant Instructions

1. **NEVER** use pip commands - only pipx or homebrew.
1. When creating new features, copy the patterns from existing roles like `dns` or `services` rather than inventing new approaches.

## Role Checklist (apply to every role when reviewing or fixing)

When working on any role, always go through these steps in order:

1. **`gather_facts: false`** — Verify all 3 playbooks (`backup`, `create-from-backup`, `create-from-minimal`) have `gather_facts: false`.
2. **Minimal fields** — Check the existing hand-crafted `.json` files in `backup/root/<role>/` to determine the correct minimal keys. The union of all keys across all files is the baseline.
3. **`vars/main.yml`** — Verify the file exists in `roles/<role>/vars/main.yml` with the `<role>_minimal_keys` list. Without it, the backup silently skips saving `.json` files.
4. **`backup.yml`** — Verify it uses `path_common_firewall_save_backup_files` with `minimal_keys` set, and applies `remove_keys` for `invalid_attribute`. Add `replace_keys` for any keys the Ansible module renames (e.g. `interface-name` → `interface_name`).
5. **`create-from-backup.yml` and `create-from-minimal.yml`** — Verify they use `path_common_firewall_get_backup_files`, loop with `loop_var: file`, and call `add-entry.yml`.
6. **`add-entry.yml` — space-separated fields** — Check for fields that the FortiGate API returns as a space-separated string but the module expects as a list (e.g. `allowaccess`). Fix with `.split(' ') | select() | list`.
7. **`add-entry.yml` — hyphenated sub-dict keys** — Check for nested dicts (e.g. `ipv6`, `phy_setting`) that contain hyphenated keys. The `.bkp` file will have them renamed by `backup.yml`, so `add-entry.yml` must read the underscored versions. Use the `hyphen_to_underscore` filter in `backup.yml` and matching underscored key access in `add-entry.yml`.
8. **`add-entry.yml` — missing fields** — Cross-check fields against the module's `.keys` files (if present) and the `.bkp` files to ensure no important parameters are omitted.
9. **Run all 3 playbooks** — Use full output (no `tail`/`grep` truncation) so failures are visible. Run backup first, then create-from-minimal, then create-from-backup.
10. **API limitations** — Note any resources the FortiGate API cannot create programmatically (e.g. loopback interfaces require manual UI/CLI creation first).
