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

1. Save the password that Zabbix will use to collect events and metrics from the firewall.

    ```bash
    secret-tool store --label="edge-firewall-01-snmp-password" password "edge-firewall-01-snmp-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-01-snmp-password"
    ```

1. This repository have git submodule, run this command to download all of them:
    ```bash
    git submodule update --init --recursive
    ```

1. Prepare the Ubuntu machine to run Ansible playbooks:
    ```bash
    ansible-playbook 01-control-machine.yml -K
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

1. Backup and create SNMP settings:
    ```bash
    ansible-playbook 11-snmp-backup.yml
    ansible-playbook 11-snmp-create.yml
    ```

1. Backup and create global system settings:
    ```bash
    ansible-playbook 12-system-settings-backup.yml
    ansible-playbook 12-system-settings-create.yml
    ```

1. Backup and create NTP system settings:
    ```bash
    ansible-playbook 13-ntp-backup.yml
    ansible-playbook 13-ntp-create.yml
    ```

1. Backup and create DHCP system settings:
    ```bash
    ansible-playbook 14-dhcp-backup.yml
    ansible-playbook 14-dhcp-create.yml
    ```

1. Backup and create Syslog system settings:
    ```bash
    ansible-playbook 15-syslog-backup.yml
    ansible-playbook 15-syslog-create.yml
    ```

1. Backup and create Firewall DOS Policy system settings:
    ```bash
    ansible-playbook 16-firewall-dos-policy-backup.yml
    ansible-playbook 16-firewall-dos-policy-create.yml
    ```

1. Backup and create Firewall DOS Policy system settings:
    ```bash
    ansible-playbook 16-firewall-dos-policy-backup.yml
    ansible-playbook 16-firewall-dos-policy-create.yml
    ```

1. Backup and create Firewall Central SNAT system settings:
    ```bash
    ansible-playbook 17-firewall-central-snat-backup.yml
    ansible-playbook 17-firewall-central-snat-create.yml
    ```

1. Backup and create System SDWAN system settings:
    ```bash
    ansible-playbook 18-system-sdwan-backup.yml
    ansible-playbook 18-system-sdwan-create.yml
    ```

1. Backup and create System VDOM system settings:
    ```bash
    ansible-playbook 19-system-vdom-backup.yml
    ansible-playbook 19-system-vdom-create.yml
    ```

1. Backup and create Static Routes settings:
    ```bash
    ansible-playbook 20-static-route-backup.yml
    ansible-playbook 20-static-route-create.yml
    ```

1. Run all other playbooks in one execution:
    ```bash
    ansible-playbook site-backup.yml
    ansible-playbook site-create.yml
    ```

### Created by:

Luciano Sampaio.
