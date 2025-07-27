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

1. Save the password for the private key of the SSL certificate used by the firewall admin interface.

    ```bash
    secret-tool store --label="edge-firewall-ssl-password" password "edge-firewall-ssl-password"
    ```

1. Confirm the password was correctly saved in the secret manager:
    ```bash
    secret-tool lookup password "edge-firewall-ssl-password"
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

1. Upload SSL certificate to the firewall:
    ```bash
    ansible-playbook 05-certificate-upload.yml
    ```

1. Backup and create global system settings:
    ```bash
    ansible-playbook 06-system-settings-backup.yml
    ansible-playbook 06-system-settings-create-from-backup.yml
    ansible-playbook 06-system-settings-create-from-minimal.yml
    ```

1. Backup and create DNS settings:
    ```bash
    ansible-playbook 07-dns-backup.yml
    ansible-playbook 07-dns-create-from-backup.yml
    ansible-playbook 07-dns-create-from-minimal.yml
    ```

1. Backup and create NTP system settings:
    ```bash
    ansible-playbook 08-ntp-backup.yml
    ansible-playbook 08-ntp-create-from-backup.yml
    ansible-playbook 08-ntp-create-from-minimal.yml
    ```

1. Backup and create interfaces:
    ```bash
    ansible-playbook 09-system-interface-backup.yml
    ansible-playbook 09-system-interface-create-from-backup.yml
    ansible-playbook 09-system-interface-create-from-minimal.yml
    ```

1. Backup and create system zones:
    ```bash
    ansible-playbook 10-system-zone-backup.yml
    ansible-playbook 10-system-zone-create-from-backup.yml
    ansible-playbook 10-system-zone-create-from-minimal.yml
    ```

1. Backup and create firewall addresses:
    ```bash
    ansible-playbook 11-firewall-address-backup.yml
    ansible-playbook 11-firewall-address-create-from-backup.yml
    ansible-playbook 11-firewall-address-create-from-minimal.yml
    ```

1. Backup and create services:
    ```bash
    ansible-playbook 12-services-backup.yml
    ansible-playbook 12-services-create-from-backup.yml
    ansible-playbook 12-services-create-from-minimal.yml
    ```

1. Backup and create static routes:
    ```bash
    ansible-playbook 13-static-route-backup.yml
    ansible-playbook 13-static-route-create-from-backup.yml
    ansible-playbook 13-static-route-create-from-minimal.yml
    ```

1. Backup and create SDWAN settings:
    ```bash
    ansible-playbook 14-system-sdwan-backup.yml
    ansible-playbook 14-system-sdwan-create-from-backup.yml
    ansible-playbook 14-system-sdwan-create-from-minimal.yml
    ```

1. Backup and create Central SNAT settings:
    ```bash
    ansible-playbook 15-firewall-central-snat-backup.yml
    ansible-playbook 15-firewall-central-snat-create-from-backup.yml
    ansible-playbook 15-firewall-central-snat-create-from-minimal.yml
    ```

1. Backup and create LDAP settings:
    ```bash
    ansible-playbook 16-ldap-backup.yml
    ansible-playbook 16-ldap-create-from-backup.yml
    ansible-playbook 16-ldap-create-from-minimal.yml
    ```

1. Backup and create firewall policies:
    ```bash
    ansible-playbook 17-firewall-policy-backup.yml
    ansible-playbook 17-firewall-policy-create-from-backup.yml
    ansible-playbook 17-firewall-policy-create-from-minimal.yml
    ```

1. Backup and create DHCP system settings:
    ```bash
    ansible-playbook 18-dhcp-backup.yml
    ansible-playbook 18-dhcp-create-from-backup.yml
    ansible-playbook 18-dhcp-create-from-minimal.yml
    ```

1. Backup and create Syslog system settings:
    ```bash
    ansible-playbook 19-syslog-backup.yml
    ansible-playbook 19-syslog-create-from-backup.yml
    ansible-playbook 19-syslog-create-from-minimal.yml
    ```

1. Backup and create SNMP system settings:
    ```bash
    ansible-playbook 20-snmp-backup.yml
    ansible-playbook 20-snmp-create-from-backup.yml
    ansible-playbook 20-snmp-create-from-minimal.yml
    ```

1. Backup and create Firewall DOS Policy system settings:
    ```bash
    ansible-playbook 21-firewall-dos-policy-backup.yml
    ansible-playbook 21-firewall-dos-policy-create-from-backup.yml
    ansible-playbook 21-firewall-dos-policy-create-from-minimal.yml
    ```

1. Run all other playbooks in one execution:
    ```bash
    ansible-playbook site-backup.yml
    ansible-playbook site-create-from-backup.yml
    ansible-playbook site-create-from-minimal.yml
    ```

### Created by:

Luciano Sampaio.
