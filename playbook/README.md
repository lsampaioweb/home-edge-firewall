# Setting up a Fortigate with Ansible playbooks

Run these commands on the computer running Ansible:

1. Save the password for each Fortigate in the secret manager.

    - This is necessary to avoid putting any credentials in the source code.
    - For example, to save the password for 'firewall-01' use this command:
      ```bash
      secret-tool store --label="firewall-01_usr_admin" password "firewall-01_usr_admin"
      ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "firewall-01_usr_admin"
        ```

1. Save the password for the private key of the SSL certificate used by the firewall admin interface.

    ```bash
    secret-tool store --label="lan.home/prd/firewall-01.lan.home" password "lan.home/prd/firewall-01.lan.home"
    ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "lan.home/prd/firewall-01.lan.home"
        ```

1. Save the password that the firewall will use to send email notifications to the SMTP server.

    ```bash
    secret-tool store --label="firewall-01_smtp_password" password "firewall-01_smtp_password"
    ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "firewall-01_smtp_password"
        ```

1. Save the password that SNMP clients will use to connect to the firewall.

    ```bash
    secret-tool store --label="firewall-01_snmp_password" password "firewall-01_snmp_password"
    ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "firewall-01_snmp_password"
        ```

1. Save the password that Zabbix will use to collect events and metrics from the firewall.

    ```bash
    secret-tool store --label="firewall-01_usr_zabbix" password "firewall-01_usr_zabbix"
    ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "firewall-01_usr_zabbix"
        ```

1. Change to the playbook directory:
    ```bash
    cd playbook/
    ```

1. **After a factory reset**, the FortiGate's DNS server is not running yet, so `firewall-01.lan.home` won't resolve.

    - Add a temporary entry to `/etc/hosts` on the control machine (requires sudo in a regular terminal):
      ```bash
      sudo sh -c 'echo "192.168.4.1 firewall.lan.home firewall-01.lan.home" >> /etc/hosts'
      ```

    - Keep `inventory/hosts` using the bare hostname (no `ansible_host` override) so that Ansible connects using the hostname, which matches the SSL certificate CN.

      After playbook 07 (DNS) has run and the FortiGate's DNS server is resolving `lan.home` correctly, remove the `/etc/hosts` entry:
      ```bash
      sudo sed -i '/firewall.*lan\.home/d' /etc/hosts
      ```

1. **After a factory reset**, the FortiGate has a self-signed SSL certificate that Ansible cannot verify.

    - Temporarily enable certificate bypass in `inventory/hosts` by setting:
      ```
      ansible_httpapi_validate_certs=false
      ```

      After playbook `05-certificate-upload.yml` has completed successfully, remove this line (or set it back to `false` commented out) to restore strict certificate validation.

1. Prepare the Ubuntu machine to run Ansible playbooks:

    - This requires `sudo`. Run it from a regular system terminal, not from inside VS Code (the VS Code integrated terminal blocks privilege escalation).

      This only needs to be run once per machine — skip it if Ansible and the `fortinet.fortios` collection are already installed.
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

1. Configure the ACME client to use a custom Certificate Authority (e.g., HCP Vault):
    ```bash
    ansible-playbook 05-certificate-acme.yml
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

1. Backup and create LDAP settings:
    ```bash
    ansible-playbook 08-ldap-backup.yml
    ansible-playbook 08-ldap-create-from-backup.yml
    ansible-playbook 08-ldap-create-from-minimal.yml
    ```

1. Backup and create interfaces:
    ```bash
    ansible-playbook 09-system-interface-backup.yml
    ansible-playbook 09-system-interface-create-from-backup.yml
    ansible-playbook 09-system-interface-create-from-minimal.yml
    ```

1. Backup and create DNS Server on Interface settings *(role to be created)*:
    ```bash
    ansible-playbook 10-dns-server-backup.yml
    ansible-playbook 10-dns-server-create-from-backup.yml
    ansible-playbook 10-dns-server-create-from-minimal.yml
    ```

1. Backup and create NTP system settings:
    ```bash
    ansible-playbook 11-ntp-backup.yml
    ansible-playbook 11-ntp-create-from-backup.yml
    ansible-playbook 11-ntp-create-from-minimal.yml
    ```

1. Backup and create system zones:
    ```bash
    ansible-playbook 12-system-zone-backup.yml
    ansible-playbook 12-system-zone-create-from-backup.yml
    ansible-playbook 12-system-zone-create-from-minimal.yml
    ```

1. Backup and create DHCP system settings:
    ```bash
    ansible-playbook 13-dhcp-backup.yml
    ansible-playbook 13-dhcp-create-from-backup.yml
    ansible-playbook 13-dhcp-create-from-minimal.yml
    ```

1. Backup and create SDWAN settings:
    ```bash
    ansible-playbook 14-system-sdwan-backup.yml
    ansible-playbook 14-system-sdwan-create-from-backup.yml
    ansible-playbook 14-system-sdwan-create-from-minimal.yml
    ```

1. Backup and create static routes:
    ```bash
    ansible-playbook 15-static-route-backup.yml
    ansible-playbook 15-static-route-create-from-backup.yml
    ansible-playbook 15-static-route-create-from-minimal.yml
    ```

1. Backup and create services:
    ```bash
    ansible-playbook 16-services-backup.yml
    ansible-playbook 16-services-create-from-backup.yml
    ansible-playbook 16-services-create-from-minimal.yml
    ```

1. Backup and create Syslog system settings:
    ```bash
    ansible-playbook 17-syslog-backup.yml
    ansible-playbook 17-syslog-create-from-backup.yml
    ansible-playbook 17-syslog-create-from-minimal.yml
    ```

1. Backup and create SNMP system settings:
    ```bash
    ansible-playbook 18-snmp-backup.yml
    ansible-playbook 18-snmp-create-from-backup.yml
    ansible-playbook 18-snmp-create-from-minimal.yml
    ```

1. Backup and create firewall addresses:
    ```bash
    ansible-playbook 19-firewall-address-backup.yml
    ansible-playbook 19-firewall-address-create-from-backup.yml
    ansible-playbook 19-firewall-address-create-from-minimal.yml
    ```

1. Backup and create Central SNAT settings:
    ```bash
    ansible-playbook 20-firewall-central-snat-backup.yml
    ansible-playbook 20-firewall-central-snat-create-from-backup.yml
    ansible-playbook 20-firewall-central-snat-create-from-minimal.yml
    ```

1. Backup and create Firewall DOS Policy settings:
    ```bash
    ansible-playbook 21-firewall-dos-policy-backup.yml
    ansible-playbook 21-firewall-dos-policy-create-from-backup.yml
    ansible-playbook 21-firewall-dos-policy-create-from-minimal.yml
    ```

1. Backup and create firewall policies:
    ```bash
    ansible-playbook 22-firewall-policy-backup.yml
    ansible-playbook 22-firewall-policy-create-from-backup.yml
    ansible-playbook 22-firewall-policy-create-from-minimal.yml
    ```

1. Backup and create Email Server settings:
    ```bash
    ansible-playbook 23-email-server-backup.yml
    ansible-playbook 23-email-server-create-from-backup.yml
    ansible-playbook 23-email-server-create-from-minimal.yml
    ```

1. Backup and create Alert Email settings:
    ```bash
    ansible-playbook 24-alertemail-backup.yml
    ansible-playbook 24-alertemail-create-from-backup.yml
    ansible-playbook 24-alertemail-create-from-minimal.yml
    ```

1. Run all other playbooks in one execution:
    ```bash
    ansible-playbook site-backup.yml
    ansible-playbook site-create-from-backup.yml
    ansible-playbook site-create-from-minimal.yml
    ```

1. Create Ansible attributes for all firewall Ansible modules:
    ```bash
    ansible-playbook 30-ansible-attributes-create.yml
    ```

### Created by:

Luciano Sampaio.
