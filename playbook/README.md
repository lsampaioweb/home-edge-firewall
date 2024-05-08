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
ansible-playbook 01-control-machine.yml
ansible-playbook 02-backup.yml
ansible-playbook 03-restore.yml
ansible-playbook 04-dns.yml
ansible-playbook 05-firewall-address.yml
ansible-playbook 06-system-settings.yml

# You can use tags in order to run only backup or create tasks.
--tags "backup,untagged"
--tags "backup,untagged,debug"

--tags "create,untagged"
--tags "create,untagged,debug"
```

#
### Roles you can execute:
1. [Setup](roles/control_machine/README.md) the control machine to run Ansible scripts.

#
### Created by:

1. Luciano Sampaio.
