```text
Name                : Home-To-Staging-Monitor
Incoming Interface  : zone-home
Outgoing Interface  : zone-staging
Source              : LAG-Home address
Destination         : vs-monitor-subnet
Schedule            : always
Service             : PING, SSH
Action              : ACCEPT

Firewall/Network Options
  Passive Health Check  : Unchecked
  Protocol Options      : default

Security Profiles
  AntiVirus               : Unchecked
  Web Filter              : Unchecked
  DNS Filter              : Unchecked
  Application Control     : Unchecked
  IPS                     : Unchecked
  File Filter             : Unchecked
  SSL Inspection          : Unchecked
  certificate-inspection  : Unchecked

Logging Options
  Log Allowed Traffic : All Sessions

Enable this policy: Checked
```