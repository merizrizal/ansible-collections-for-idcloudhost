# Module: vm

Manages VM lifecycle, resizing, and power state.

## Key options
- `api_key` (required, string, no_log)
- `location` (required, string, choices: `jkt01`, `jkt02`, `jkt03`, `sgp01`)
- `name` (required, string)
- `state` (optional, default: `present`, choices: `present`, `resize`, `active`, `inactive`, `absent`)
- `network_name` (required when `state=present`)
- `os_name` (required when `state=present`)
- `os_version` (required when `state=present`)
- `disks` (required when `state=present` or `state=resize`)
- `vcpu` (required when `state=present` or `state=resize`)
- `ram` (required when `state=present` or `state=resize`)
- `username` (required when `state=present`)
- `password` (required when `state=present`, no_log)
- `remove_public_ipv4` (required when `state=absent`)

## Behavior
- `present`: creates a VM when it does not exist. Validates `os_name` and `os_version` compatibility.
- `resize`: stops the VM, resizes RAM/VCPU and disks, then starts the VM again.
- `active`: powers on the VM.
- `inactive`: powers off the VM.
- `absent`: deletes the VM, optionally removing the public IPv4 if `remove_public_ipv4=true`.

## Returns
- `uuid`
- `name`
- `hostname`
- `private_ipv4`
- `public_ipv4`
- `disks`
- `disk_uuid`
- `vcpu`
- `ram`
- `billing_account`
- `status`
