# Ansible Collection - merizrizal.idcloudhost

An Ansible collection for automating IDCloudHost resources such as VPC networks, VMs, floating IPs, and block storage.

**Collection path:** `merizrizal/idcloudhost`

## Requirements
- Ansible `>=2.15.0` (from `merizrizal/idcloudhost/meta/runtime.yml`)
- Python `requests` module on the controller
- `yq` for the `make install` target
- An IDCloudHost API key

## Install (local build)
```bash
source envrc
make install
```

## Quickstart
### Inventory
```yaml
---
target:
  children:
    idch:
      hosts:
        api.idcloudhost.com:
          ansible_connection: httpapi
          ansible_httpapi_use_ssl: true
          ansible_httpapi_validate_certs: true
```

### Playbook examples
Create a VPC network:
```yaml
- name: Create VPC network
  hosts: idch
  tasks:
    - name: Create network
      merizrizal.idcloudhost.network:
        api_key: "{{ your_api_key }}"
        name: "{{ your_desired_network_name }}"
        location: jkt02
        state: present
```

Create a VM:
```yaml
- name: Create VM
  hosts: idch
  tasks:
    - name: Create VM resource
      merizrizal.idcloudhost.vm:
        api_key: "{{ your_api_key }}"
        location: jkt02
        network_name: "{{ your_desired_network_name }}"
        name: "{{ your_desired_vm_name }}"
        os_name: ubuntu
        os_version: 24.04-lts
        disks: 20
        vcpu: 2
        ram: 2048
        username: admin
        password: My4adminpass
        state: present
```

## Module reference
Use `ansible-doc` for the full module documentation:
- `ansible-doc merizrizal.idcloudhost.network`
- `ansible-doc merizrizal.idcloudhost.vm`
- `ansible-doc merizrizal.idcloudhost.floating_ip`
- `ansible-doc merizrizal.idcloudhost.block_storage`
- `ansible-doc merizrizal.idcloudhost.get_public_ip`

## Documentation
Additional documentation is in the `docs/` directory.
