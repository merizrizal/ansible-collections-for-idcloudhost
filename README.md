## Repository for Ansible Collection - merizrizal.idcloudhost

### Requirements:
- Install `yq` from https://github.com/mikefarah/yq

Do `make install` for installing into ansible collections directory.


### How to implement it
Write the inventory.yml. For example:
```
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

Then write the playbook.yml file.

Example for creating network resource.
```
---
- name: ID Cloud Host Setup
  hosts: idch
  tasks:
    - name: Create network resource
      merizrizal.idcloudhost.create_network:
        api_key: "{{ your_api_key }}"
        name: "{{ your_desired_network_name }}"
        location: jkt02
```
To see the module documention, run `ansible-doc merizrizal.idcloudhost.create_network`

Example for creating a new VM.
```
---
- name: Get network resource
  merizrizal.idcloudhost.get_network:
    api_key: "{{ your_api_key }}"
    location: jkt02
  register: get_network_result

- name: Create VM
  merizrizal.idcloudhost.create_vm:
    api_key: "{{ your_api_key }}"
    location: jkt02
    network_uuid: "{{ get_network_result.uuid }}"
    name: vm_created_by_ansible
    os_name: ubuntu
    os_version: 24.04-lts
    disks: 20
    vcpu: 2
    ram: 2048
    username: admin
    password: My4adminpass
```
To see the module documention, run `ansible-doc merizrizal.idcloudhost.get_network` and `ansible-doc merizrizal.idcloudhost.create_vm`