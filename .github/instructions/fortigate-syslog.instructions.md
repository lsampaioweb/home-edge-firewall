---
description: "Use when changing FortiGate Syslog destination or source settings. Covers DNS resolution, source-interface addressing, and the boundary between minimal settings and log filters."
applyTo: "ansible/backup/*/syslog/*.json"
---

# FortiGate Syslog

## Establish The Baseline

- Read the target VDOM's Syslog JSON, paired capture, relevant Syslog documentation, and the role's minimal-key filter and importer.
- Verify the destination hostname or address, transport, port, facility, status, and source IP against the request.
- If `server` is an FQDN, check the intended DNS zone or other documented resolver source. If `source-ip` is set, verify it matches an address on an existing interface.

## Check Related Configuration

- Before changing an interface address, search Syslog JSON for a matching `source-ip` and update it only when required by the requested behavior.
- The minimal Syslog filter retains facility, format, mode, port, server, source IP, and status. `add-entry.yml` maps additional setting fields, but fields outside the filter are not retained by minimal backup generation; log filters are a separate configuration workflow.
- Do not add a DNS record or alter log filters unless requested and supported by the corresponding configuration workflow.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify the source IP, destination reference, and supported fields against current target-VDOM configuration.
- Verify the current Syslog import playbook and inventory, then syntax-check it. Do not execute live imports unless requested.
- State configuration validation separately from live Syslog delivery testing.
