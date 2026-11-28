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
    secret-tool store --label="lan.home/prd/firewall.lan.home" password "lan.home/prd/firewall.lan.home"
    ```

    - Confirm the password was correctly saved in the secret manager:
        ```bash
        secret-tool lookup password "lan.home/prd/firewall.lan.home"
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

1. Change to the Ansible directory:
    ```bash
    cd ansible/
    ```

1. **After a factory reset only**: perform these two bootstrap steps before running any playbook:

    - Add a temporary entry to `/etc/hosts` so `firewall-01.lan.home` resolves (requires sudo — run from a regular terminal, not the VS Code integrated terminal):
      ```bash
      sudo sh -c 'echo "192.168.4.1 firewall.lan.home firewall-01.lan.home" >> /etc/hosts'
      ```

    - Uncomment the certificate bypass line in `inventory/hosts`:
      ```bash
      sed -i 's/^# ansible_httpapi_validate_certs=false/ansible_httpapi_validate_certs=false/' inventory/hosts
      ```

1. All playbooks accept `tags` to print extra information in the output:
    ```bash
    ansible-playbook xxx.yml --tags "untagged,debug"
    ```

    - Debug-tagged tasks may print sensitive data. Setting `debug=true` also disables `no_log` for the certificate upload.

1. Prepare the Ubuntu machine to run Ansible playbooks:

    - This requires `sudo`. Run it from a regular system terminal, not from inside VS Code (the VS Code integrated terminal blocks privilege escalation).

      This only needs to be run once per machine — skip it if Ansible and the `fortinet.fortios` collection are already installed.
      ```bash
      ansible-playbook 01-control-machine.yml -K
      ```

1. These playbooks perform system backups and restores:
    - Backup all settings. The configured retention is the latest 10 global backup files (`backup_files_to_keep`).
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

1. **After a factory reset only**: the trusted SSL certificate is now installed. Restore strict certificate validation by commenting the bypass back out in `inventory/hosts`:
    ```bash
    sed -i 's/^ansible_httpapi_validate_certs=false/# ansible_httpapi_validate_certs=false/' inventory/hosts
    ```

1. Backup and create global system settings:
    ```bash
    ansible-playbook 06-system-settings-backup.yml
    ansible-playbook 06-system-settings-create-from-backup.yml
    ansible-playbook 06-system-settings-create-from-minimal.yml
    ```

1. Backup and create interfaces:
    ```bash
    ansible-playbook 07-system-interface-backup.yml
    ansible-playbook 07-system-interface-create-from-backup.yml
    ansible-playbook 07-system-interface-create-from-minimal.yml
    ```

1. Manage DNS database settings:

    The backup downloads the firewall's DNS zones and overwrites matching saved `.json` and `.bkp` files. Preserve any unapplied changes before running it.
    ```bash
    ansible-playbook 08-dns-backup.yml
    ```

    To restore saved full captures, run:
    ```bash
    ansible-playbook 08-dns-create-from-backup.yml
    ```

    To apply saved minimal definitions, run the following playbook. It processes all saved DNS zone definitions, not only the edited zone.
    ```bash
    ansible-playbook 08-dns-create-from-minimal.yml
    ```

1. Backup and create DNS Server on Interface settings:
    ```bash
    ansible-playbook 09-dns-server-backup.yml
    ansible-playbook 09-dns-server-create-from-backup.yml
    ansible-playbook 09-dns-server-create-from-minimal.yml
    ```

1. **After a factory reset only**: the FortiGate DNS server is now running and resolving `lan.home`. Remove the temporary `/etc/hosts` entry:
    ```bash
    sudo sed -i '/firewall.*lan\.home/d' /etc/hosts
    ```

1. Backup and create NTP system settings:
    ```bash
    ansible-playbook 10-ntp-backup.yml
    ansible-playbook 10-ntp-create-from-backup.yml
    ansible-playbook 10-ntp-create-from-minimal.yml
    ```

1. Backup and create LDAP settings:
    ```bash
    ansible-playbook 11-ldap-backup.yml
    ansible-playbook 11-ldap-create-from-backup.yml
    ansible-playbook 11-ldap-create-from-minimal.yml
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

1. Backup and create firewall addresses:
    ```bash
    ansible-playbook 17-firewall-address-backup.yml
    ansible-playbook 17-firewall-address-create-from-backup.yml
    ansible-playbook 17-firewall-address-create-from-minimal.yml
    ```

1. Backup and create Central SNAT settings:
    ```bash
    ansible-playbook 18-firewall-central-snat-backup.yml
    ansible-playbook 18-firewall-central-snat-create-from-backup.yml
    ansible-playbook 18-firewall-central-snat-create-from-minimal.yml
    ```

1. Backup and create Firewall DOS Policy settings:
    ```bash
    ansible-playbook 19-firewall-dos-policy-backup.yml
    ansible-playbook 19-firewall-dos-policy-create-from-backup.yml
    ansible-playbook 19-firewall-dos-policy-create-from-minimal.yml
    ```

1. Backup and create firewall policies:
    ```bash
    ansible-playbook 20-firewall-policy-backup.yml
    ansible-playbook 20-firewall-policy-create-from-backup.yml
    ansible-playbook 20-firewall-policy-create-from-minimal.yml
    ```

1. Review saved firewall policy captures for `all` source and destination addresses:
    ```bash
    ansible-playbook 20-firewall-policy-review.yml
    ```

    The review reads saved `.bkp` files, not the live firewall or minimal JSON. Findings do not fail the playbook; unreadable or invalid input does. To accept a specific finding, provide its VDOM, policy ID, check and reason:
    ```bash
    ansible-playbook 20-firewall-policy-review.yml -e '{"firewall_policy_review_exceptions":[{"vdom":"root","policy_id":14,"check":"POLICY_ALL_ALL","reason":"Approved internet access"}]}'
    ```

1. Backup and create Email Server settings:
    ```bash
    ansible-playbook 21-email-server-backup.yml
    ansible-playbook 21-email-server-create-from-backup.yml
    ansible-playbook 21-email-server-create-from-minimal.yml
    ```

1. Backup and create Alert Email settings:
    ```bash
    ansible-playbook 22-alertemail-backup.yml
    ansible-playbook 22-alertemail-create-from-backup.yml
    ansible-playbook 22-alertemail-create-from-minimal.yml
    ```

1. Backup and create Syslog system settings:
    ```bash
    ansible-playbook 23-syslog-backup.yml
    ansible-playbook 23-syslog-create-from-backup.yml
    ansible-playbook 23-syslog-create-from-minimal.yml
    ```

1. Backup and create SNMP system settings:
    ```bash
    ansible-playbook 24-snmp-backup.yml
    ansible-playbook 24-snmp-create-from-backup.yml
    ansible-playbook 24-snmp-create-from-minimal.yml
    ```

1. Create Ansible attributes for all firewall Ansible modules:
    ```bash
    ansible-playbook 30-ansible-attributes-create.yml
    ```

1. Run all other playbooks in one execution:
    ```bash
    ansible-playbook site-backup.yml
    ansible-playbook site-create-from-backup.yml
    ansible-playbook site-create-from-minimal.yml
    ```

### Adding VLANs

Run the following commands from `ansible/`, using `inventory/hosts`.

A new VLAN requires more than an interface definition. Compare an existing VLAN
in the same VDOM and environment, then add or update all six configuration areas:

| Area | Definition under `backup/<vdom>/` |
| --- | --- |
| VLAN interface | `system_interface/vlan/<vlan>.json` |
| DHCP scope | `dhcp/<id>-<vlan>.json` |
| Interface DNS service | `dns_server/<vlan>.json` |
| NTP server interface membership | `ntp/*.json` |
| Zone membership | `system_zone/*.json` |
| Subnet address object | `firewall_address/<vlan>-subnet.json` |

Preserve existing shared-list members, zone isolation, and referenced interface
names. A VLAN ID does not establish its subnet or parent interface. Do not copy
staging addressing into production.

Apply the minimal definitions in dependency order:

```bash
ansible-playbook -i inventory/hosts \
    07-system-interface-create-from-minimal.yml \
    09-dns-server-create-from-minimal.yml \
    10-ntp-create-from-minimal.yml \
    12-system-zone-create-from-minimal.yml \
    13-dhcp-create-from-minimal.yml \
    17-firewall-address-create-from-minimal.yml
```

Each playbook processes all matching saved definitions in its area, not only the
new VLANs. Add `--syntax-check` to validate the playbooks without applying them.
Also validate JSON, unique IDs, subnet overlap, DHCP ranges, and cross-file
references before importing.

Service configuration does not grant access between VLANs. Review existing
zone-wide coverage separately from application-specific policy permissions.

### DHCP NTP settings

System NTP server membership and DHCP NTP advertisement are separate settings.
The VS and VP VLAN scopes use `"ntp-service": "local"` so DHCP clients are told to
use the FortiGate's IP on their VLAN. The system NTP configuration must also have
server mode enabled and include that interface.

| DHCP option | JSON value | Client NTP server |
| --- | --- | --- |
| Local | `local` | FortiGate interface IP on the client VLAN |
| Same as System NTP | `default` | Upstream NTP servers configured for the FortiGate |
| Specify | `specify` | Addresses configured in `ntp-server1` through `ntp-server3` |

Use `specify` only with usable server addresses. The `0.0.0.0` server fields are
unused when the mode is `local`. Clients must support DHCP-provided NTP settings
and may need a lease renewal to receive changes.

For DHCP-only changes, run:

```bash
ansible-playbook 13-dhcp-create-from-minimal.yml -i inventory/hosts
```

### Backup files

Minimal `.json` files are consumed by `create-from-minimal` playbooks. Full `.bkp`
files are captured device configuration consumed by `create-from-backup`
playbooks; do not fabricate them to represent desired settings.

Backup playbooks regenerate both formats from device data. Apply pending minimal
changes before running a backup, or preserve them separately, because a backup
can overwrite unapplied edits. The DHCP minimal filter retains the NTP mode and
all three explicit NTP server fields.

After applying DHCP changes, refresh the captured configuration with:

```bash
ansible-playbook 13-dhcp-backup.yml -i inventory/hosts
```

Comparing a regenerated minimal file with its full backup confirms consistency,
not that the previous desired configuration was applied. Compare against a saved
pre-import version as well. Configuration checks do not replace live client
DHCP, DNS, NTP, and connectivity tests.

### Created by:

Luciano Sampaio.
