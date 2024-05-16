# Setting up a Fortigate with Ansible playbooks

Run these commands on the computer running Ansible:

1. Save the password for each Fortigate in the secret manager.

    - This is necessary to avoid putting any credentials in the source code.
    - For example, to save the password for 'edge-firewall-01':
    ```bash
    secret-tool store --label="edge-firewall-01-admin-password" password "edge-firewall-01-admin-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-01-admin-password"
    ```

1. Prepare the Ubuntu machine to run Ansible playbooks:
    ```bash
    ansible-playbook 01-control-machine.yml
    ```

1. All playbooks accept `tags` to print extra information in the output:
    ```bash
    ansible-playbook xxx.yml --tags "untagged,debug"
    ```

1. These playbooks perform system backups and restores:
    - Backup all settings. It will keep only the latest 5 files.
    ```bash
    ansible-playbook 02-backup.yml
    ```

    - CAUTION: This playbook reboots the firewall. Use with care:
    ```bash
    ansible-playbook 03-restore.yml
    ```

1. Backup and create DNS settings:
    ```bash
    ansible-playbook 04-dns-backup.yml
    ansible-playbook 04-dns-create.yml
    ```

1. Backup and create firewall addresses:
    ```bash
    ansible-playbook 05-firewall-address-backup.yml
    ansible-playbook 05-firewall-address-create.yml
    ```

1. Backup and create services:
    ```bash
    ansible-playbook 06-services-backup.yml
    ansible-playbook 06-services-create.yml
    ```

1. Backup and create interfaces:
    ```bash
    ansible-playbook 07-system-interface-backup.yml
    ansible-playbook 07-system-interface-create.yml
    ```

1. Backup and create zones:
    ```bash
    ansible-playbook 08-system-zone-backup.yml
    ansible-playbook 08-system-zone-create.yml
    ```

1. Backup and create firewall policies:
    ```bash
    ansible-playbook 09-firewall-policy-backup.yml
    ansible-playbook 09-firewall-policy-create.yml
    ```

1. Backup and create LDAP settings:
    ```bash
    ansible-playbook 10-ldap-backup.yml
    ansible-playbook 10-ldap-create.yml
    ```

1. Backup and create global system settings:
    ```bash
    ansible-playbook 11-system-settings-backup.yml
    ansible-playbook 11-system-settings-create.yml
    ```

1. Run all other playbooks in one execution:
    ```bash
    ansible-playbook site-backup.yml
    ansible-playbook site-restore.yml
    ```

### Created by:

Luciano Sampaio.
