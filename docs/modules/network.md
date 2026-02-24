# Module: network

Manages VPC networks in a selected location.

## Key options
- `api_key` (required, string, no_log)
- `name` (required, string)
- `location` (required, string, choices: `jkt01`, `jkt02`, `jkt03`, `sgp01`)
- `state` (optional, default: `present`, choices: `present`, `absent`)

## Behavior
- `present`: creates the network if it does not exist, otherwise reports `changed=false`.
- `absent`: deletes the network if it exists, otherwise reports `changed=false`.

## Returns
- `uuid`
- `name`
- `subnet`
- `is_default`
