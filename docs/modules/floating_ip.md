# Module: floating_ip

Manages floating IPv4 addresses and optional VM assignment.

## Key options
- `api_key` (required, string, no_log)
- `location` (required, string, choices: `jkt01`, `jkt02`, `jkt03`, `sgp01`)
- `name` (required, string)
- `vm_name` (optional, string)
- `state` (optional, default: `present`, choices: `present`, `absent`, `unassign`)

## Behavior
- `present`: creates a floating IP if it does not exist. If `vm_name` is provided, assigns it to the VM.
- `absent`: deletes the floating IP if it exists.
- `unassign`: detaches the floating IP from its VM if assigned.

## Returns
- `uuid`
- `name`
- `public_ipv4`
- `vm_name`
- `assigned_to_vm_uuid`
- `private_ipv4_address`
- `enabled`
