```text
Name                : Staging-To-Internet
Incoming Interface  : zone-staging
Outgoing Interface  : SD-WAN
Source              : SS-S-CLSTR address, vs-mgmt-subnet
Destination         : all
Schedule            : always
Service             : HTTP, HTTPS, PING
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