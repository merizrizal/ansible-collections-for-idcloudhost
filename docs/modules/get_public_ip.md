# Module: get_public_ip

Looks up a public IPv4 address based on either a private IPv4 or a VM UUID.

## Key options
- `api_key` (required, string, no_log)
- `location` (required, string, choices: `jkt01`, `jkt02`, `jkt03`, `sgp01`)
- `private_ipv4` (required if `vm_uuid` is not provided)
- `vm_uuid` (required if `private_ipv4` is not provided)

`private_ipv4` and `vm_uuid` are mutually exclusive; exactly one must be provided.

## Behavior
- Lists floating IPs in the selected location and returns the match for the provided `private_ipv4` or `vm_uuid`.

## Returns
- `uuid`
- `public_ipv4`
- `enabled`
- `assigned_to` (when `private_ipv4` is used)
- `assigned_to_private_ip` (when `vm_uuid` is used)
