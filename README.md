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
```
To see the module documention, run `ansible-doc merizrizal.idcloudhost.create_network`