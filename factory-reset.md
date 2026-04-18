# FortiGate 80E — Factory Reset Procedure

## Key facts

- Ubuntu interface connected to FortiGate port11: `enp4s0` (NetworkManager profile: `"Wired connection 4"`)
- FortiGate port11 IP: `192.168.4.1/24`
- Ubuntu static IP to use during reset: `192.168.4.200/24`
- **Do NOT use `sudo ip addr add`** — NetworkManager will overwrite it immediately. Always use `nmcli`.

## Command: `execute factoryreset2` (recommended)

Preserves:
  - port11 IP (`192.168.4.1`).
  - allowaccess (HTTPS, SSH).
  - system.interface.
  - system.settings.
  - VDOMs.
  - static routes.
Wipes:
  - everything else, including DHCP server on port11 and admin password.

## Command: `execute factoryreset` (full reset — wipes interfaces too)

Wipes **everything** including all interfaces (LAGs, VLANs, software switches, port11).

After reset:
  - Management interface: **`lan` hardware switch** — physical port **port12**.
  - Default IP: `192.168.1.99/24`.
  - HTTPS, SSH, PING, SNMP: enabled.

### Step 1 — Set static IP on Ubuntu (before or immediately after reset)

```bash
nmcli con mod "Wired connection 4" ipv4.addresses 192.168.4.200/24 ipv4.gateway 192.168.4.1 ipv4.method manual
nmcli con up "Wired connection 4"
```

### Step 2 — Run the factory reset via SSH

```bash
ssh admin@firewall-01.lan.home
```

In the FortiGate CLI:
```
execute factoryreset2
```

Confirm with `y`. The SSH session will drop — that is expected.

### Step 3 — Wait for reboot (~2 minutes), then verify connectivity

```bash
sudo arp -n 192.168.4.1
```

Wait until a MAC address appears. Then SSH in (the host key will have changed):

```bash
ssh-keygen -f '/home/lsampaio/.ssh/known_hosts' -R '192.168.4.1'
```

```bash
ssh admin@192.168.4.1
```


Login with username `admin` and **blank password** (just press Enter). Set a new password when prompted.

### Step 4 — Update secret-tool with the new password

```bash
secret-tool store --label="firewall-01_usr_admin" password "firewall-01_usr_admin"
```

### Step 5 — Run the site playbook

```bash
cd /home/lsampaio/Luciano/git/home/03-home-edge-firewall/playbook
```

```bash
ansible-playbook site-create-from-backup.yml
```

### Step 6 — Restore DHCP on Ubuntu (after role 12 completes)

Once the playbook finishes, revert `enp4s0` back to DHCP so it picks up a lease from the restored FortiGate DHCP server:

```bash
nmcli con mod "Wired connection 4" ipv4.addresses "" ipv4.gateway "" ipv4.method auto
```
```bash
nmcli con up "Wired connection 4"
```
