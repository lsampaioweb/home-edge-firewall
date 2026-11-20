---
description: "Use when changing FortiGate SMTP settings or alert-email recipients and filters. Covers the separate mail-server and alert settings, shared account consistency, and secret handling."
applyTo: "ansible/backup/*/system_email_server/*.json,ansible/backup/*/alertemail/*.json"
---

# FortiGate Email And Alerts

## Establish The Baseline

- Read the target VDOM's `system_email_server` and `alertemail` JSON, their paired captures, and relevant email documentation.
- Treat SMTP transport and alert recipient/filter settings as separate configuration areas. Do not assume changing one updates the other.
- When both areas use the same sender account, verify their usernames and authentication settings remain compatible.

## Handle Credentials And Recipients

- SMTP credentials are supplied through the Ansible secret lookup, not the minimal JSON. Never add, print, or request the secret in chat.
- Verify recipients, SMTP host, port, security mode, authentication, and username against the request. Do not invent recipients or weaken transport security to make delivery succeed.
- Check whether the SMTP hostname depends on a local DNS record or another documented resolver source before changing it.

## Validate Before Completion

- Parse every added or modified JSON file with a structured JSON parser.
- Verify the current minimal-key filters retain the requested fields and the importer maps them to the intended API settings.
- Verify the current import playbooks and inventory, then syntax-check affected playbooks. Do not execute live imports unless requested.
- State configuration validation separately from a live email-delivery test.
