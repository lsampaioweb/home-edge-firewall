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
ansible-playbook 04-dns-backup.yml
ansible-playbook 04-dns-create.yml

ansible-playbook 05-firewall-address.yml
ansible-playbook 05-firewall-address-backup.yml
ansible-playbook 05-firewall-address-create.yml

ansible-playbook 06-services.yml
ansible-playbook 06-services-backup.yml
ansible-playbook 06-services-create.yml

ansible-playbook 07-system-interface.yml
ansible-playbook 07-system-interface-backup.yml
ansible-playbook 07-system-interface-create.yml

ansible-playbook 08-system-zone.yml
ansible-playbook 08-system-zone-backup.yml
ansible-playbook 08-system-zone-create.yml

ansible-playbook 09-firewall-policy.yml
ansible-playbook 09-firewall-policy-backup.yml
ansible-playbook 09-firewall-policy-create.yml

ansible-playbook 10-ldap.yml
ansible-playbook 10-ldap-backup.yml
ansible-playbook 10-ldap-create.yml

ansible-playbook 11-system-settings.yml

# You can use tags in order to print extra information on the output.
--tags "untagged,debug"
```

#
### Created by:

1. Luciano Sampaio.
