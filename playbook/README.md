# Setting up a Fortigate with Ansible playbooks

Run these commands on the computer running Ansible:

1. Save the password for each Fortigate in the secret manager.

    - This is necessary to avoid putting any credentials in the source code.
    - For example, to save the password for 'edge-firewall':
    ```bash
    secret-tool store --label="edge-firewall-admin-password" password "edge-firewall-admin-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-admin-password"
    ```

1. Save the password that Zabbix will use to collect events and metrics from the firewall.

    ```bash
    secret-tool store --label="edge-firewall-zabbix-password" password "edge-firewall-zabbix-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-zabbix-password"
    ```

1. Save the password that SNMP clients will use to connect to the firewall.

    ```bash
    secret-tool store --label="edge-firewall-snmp-password" password "edge-firewall-snmp-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-snmp-password"
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

1. Backup and create VDOM settings:
    ```bash
    ansible-playbook 04-system-vdom-backup.yml
    ansible-playbook 04-system-vdom-create-from-backup.yml
    ansible-playbook 04-system-vdom-create-from-minimal.yml
    ```

1. Backup and create global system settings:
    ```bash
    ansible-playbook 05-system-settings-backup.yml
    ansible-playbook 05-system-settings-create-from-backup.yml
    ansible-playbook 05-system-settings-create-from-minimal.yml
    ```

1. Backup and create DNS settings:
    ```bash
    ansible-playbook 06-dns-backup.yml
    ansible-playbook 06-dns-create-from-backup.yml
    ansible-playbook 06-dns-create-from-minimal.yml
    ```

1. Backup and create NTP system settings:
    ```bash
    ansible-playbook 07-ntp-backup.yml
    ansible-playbook 07-ntp-create-from-backup.yml
    ansible-playbook 07-ntp-create-from-minimal.yml
    ```

1. Backup and create interfaces:
    ```bash
    ansible-playbook 08-system-interface-backup.yml
    ansible-playbook 08-system-interface-create-from-backup.yml
    ansible-playbook 08-system-interface-create-from-minimal.yml
    ```

1. Backup and create system zones:
    ```bash
    ansible-playbook 09-system-zone-backup.yml
    ansible-playbook 09-system-zone-create-from-backup.yml
    ansible-playbook 09-system-zone-create-from-minimal.yml
    ```

1. Backup and create firewall addresses:
    ```bash
    ansible-playbook 10-firewall-address-backup.yml
    ansible-playbook 10-firewall-address-create-from-backup.yml
    ansible-playbook 10-firewall-address-create-from-minimal.yml
    ```

1. Backup and create services:
    ```bash
    ansible-playbook 11-services-backup.yml
    ansible-playbook 11-services-create-from-backup.yml
    ansible-playbook 11-services-create-from-minimal.yml
    ```

1. Backup and create static routes:
    ```bash
    ansible-playbook 12-static-route-backup.yml
    ansible-playbook 12-static-route-create-from-backup.yml
    ansible-playbook 12-static-route-create-from-minimal.yml
    ```

1. Backup and create SDWAN settings:
    ```bash
    ansible-playbook 13-system-sdwan-backup.yml
    ansible-playbook 13-system-sdwan-create-from-backup.yml
    ansible-playbook 13-system-sdwan-create-from-minimal.yml
    ```

1. Backup and create Central SNAT settings:
    ```bash
    ansible-playbook 14-firewall-central-snat-backup.yml
    ansible-playbook 14-firewall-central-snat-create-from-backup.yml
    ansible-playbook 14-firewall-central-snat-create-from-minimal.yml
    ```

1. Backup and create LDAP settings:
    ```bash
    ansible-playbook 15-ldap-backup.yml
    ansible-playbook 15-ldap-create-from-backup.yml
    ansible-playbook 15-ldap-create-from-minimal.yml
    ```

1. Backup and create firewall policies:
    ```bash
    ansible-playbook 16-firewall-policy-backup.yml
    ansible-playbook 16-firewall-policy-create.yml
    ```

1. Backup and create DHCP system settings:
    ```bash
    ansible-playbook 17-dhcp-backup.yml
    ansible-playbook 17-dhcp-create.yml
    ```

1. Backup and create Syslog system settings:
    ```bash
    ansible-playbook 18-syslog-backup.yml
    ansible-playbook 18-syslog-create.yml
    ```

1. Backup and create SNMP system settings:
    ```bash
    ansible-playbook 19-snmp-backup.yml
    ansible-playbook 19-snmp-create-from-backup.yml
    ansible-playbook 19-snmp-create-from-minimal.yml
    ```

1. Backup and create Firewall DOS Policy system settings:
    ```bash
    ansible-playbook 20-firewall-dos-policy-backup.yml
    ansible-playbook 20-firewall-dos-policy-create.yml
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
