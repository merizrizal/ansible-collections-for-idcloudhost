## Repository for Ansible Collection - merizrizal.idcloudhost

### Requirements:
- Install `yq` from https://github.com/mikefarah/yq

Do `source envrc` then `make install` for installing into ansible collections directory.


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

Example of using the Network module.
```
---
- name: ID Cloud Host Setup
  hosts: idch
  tasks:
    - name: Create network VPC resource
      merizrizal.idcloudhost.network:
        api_key: "{{ your_api_key }}"
        name: "{{ your_desired_network_name }}"
        location: jkt02
        # Since the default value of state is set to present, we may exclude the state below
        state: present

    - name: Delete network VPC resource
      merizrizal.idcloudhost.network:
        api_key: "{{ your_api_key }}"
        name: "{{ your_desired_network_name }}"
        location: jkt02
        state: absent
```
To see the module documentation, run `ansible-doc merizrizal.idcloudhost.network`

Example of using the VM module.
```
---
- name: ID Cloud Host Setup
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
        # Since the default value of state is set to present, we may exclude the state below
        state: present

    - name: Resize VM
      merizrizal.idcloudhost.vm:
        api_key: "{{ your_api_key }}"
        location: jkt02
        name: "{{ your_desired_vm_name }}"
        disks: 40
        vcpu: 4
        ram: 4096
        state: resize

    - name: Power on the VM
      merizrizal.idcloudhost.vm:
        api_key: "{{ your_api_key }}"
        location: jkt02
        name: "{{ your_desired_vm_name }}"
        state: active

    - name: Power off the VM
      merizrizal.idcloudhost.vm:
        api_key: "{{ your_api_key }}"
        location: jkt02
        name: "{{ your_desired_vm_name }}"
        state: inactive

    - name: Delete VM resource
      merizrizal.idcloudhost.vm:
        api_key: "{{ your_api_key }}"
        location: jkt02
        name: "{{ your_desired_vm_name }}"
        remove_public_ipv4: false
        state: absent
```
To see the module documentation, run `ansible-doc merizrizal.idcloudhost.vm`

Other module:
- `ansible-doc merizrizal.idcloudhost.floating_ip`
- `ansible-doc merizrizal.idcloudhost.block_storage`
