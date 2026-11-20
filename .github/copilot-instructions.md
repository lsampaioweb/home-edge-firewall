# Project Guidance

- When changing a file, add an empty line at the end only if one is not already present.
- For FortiGate configuration requests, identify and read every matching topic contract in `instructions/` before editing. Search the target VDOM's minimal JSON definitions and relevant documentation for dependencies; do not assume the requested file is the only affected configuration.
- Treat minimal `*.json` files as desired configuration and `.bkp` files as captured device configuration. Do not fabricate backups or run live imports unless requested.
- When documentation conflicts with target-VDOM JSON or its paired capture, report the exact conflict and do not silently choose or copy values. Do not change configuration data or documentation to resolve a conflict unless requested.
- Before using a JSON area, verify its minimal-key filter, role task, and current import playbook support the requested field. Do not invent JSON paths or claim a field is applied if the importer omits it.
- User groups and administrator entries are documented and present in full captures, but have no minimal-JSON import role in this project. Certificates use the certificate upload workflow, not a minimal JSON area. Do not fabricate minimal definitions for these topics.
- For requests to add, import, or update FortiGate VLANs, read [the VLAN configuration contract](instructions/fortigate-vlan.instructions.md) before editing. Treat VLAN creation as a dependent configuration change, not an interface-only change.
