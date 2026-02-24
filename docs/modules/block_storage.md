# Module: block_storage

Manages VM block storage (additional disks) for a VM.

## Key options
- `api_key` (required, string, no_log)
- `location` (required, string, choices: `jkt01`, `jkt02`, `jkt03`, `sgp01`)
- `vm_name` (required, string)
- `state` (optional, default: `present`, choices: `present`, `absent`)
- `size` (required when `state=present`)
- `name` (required when `state=absent`) - disk name (e.g., `vdb`, `vdc`)

## Behavior
- `present`: creates a block storage disk and attaches it to the VM.
- `absent`: detaches and deletes a block storage disk by name from the VM.

## Returns
- `uuid`
- `name`
- `size`
- `vm_name`
