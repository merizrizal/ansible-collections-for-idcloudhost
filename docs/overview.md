# Overview

`merizrizal.idcloudhost` is an Ansible collection for managing IDCloudHost resources via their HTTP API.

## What it manages
- VPC networks
- Virtual machines (VMs)
- Floating IP addresses
- VM block storage (additional disks)
- Lookup of public IPv4 addresses

## API integration model
All modules communicate with the IDCloudHost API using the controller-side Python `requests` library. The shared logic for base URL, authentication headers, and common lookups lives in `plugins/module_utils/base.py`.

## Supported locations
The modules consistently accept one of the following location identifiers:
- `jkt01`
- `jkt02`
- `jkt03`
- `sgp01`

## Collection metadata
- Namespace: `merizrizal`
- Name: `idcloudhost`
- Version: `1.0.0`
- Required Ansible: `>=2.15.0`
