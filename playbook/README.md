# Setup a Fortigate with Ansible playbooks

Run these commands on the computer that is running Ansible:

```bash
# Save the password of each Fortigate in the secret manager.
secret-tool store --label="edge-firewall-01-admin-password" password "edge-firewall-01-admin-password"

# Confirm the password was correctly saved in the secret manager.
secret-tool lookup password "edge-firewall-01-admin-password"
```

Run the command in the terminal:
```bash
ansible-playbook site.yml
ansible-playbook 01_control_machine.yml
ansible-playbook 02_system_settings.yml
```

# Roles you can execute:
1. [Setup](roles/control_machine/README.md) the control machine to run Ansible scripts.

# Created by:

1. Luciano Sampaio.
