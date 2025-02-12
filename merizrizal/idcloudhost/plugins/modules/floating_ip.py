#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: floating_ip
short_description: Manage floating IPs
version_added: "1.0.0"

description: Manage floating IPs from a selected location.

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    location:
        description: The location name of the network to which this floating IP is assigned.
        required: true
        type: str
        choices: [ jkt01, jkt02, jkt03, sgp01 ]
    name:
        description: Name of the floating IP that will be managed.
        required: true
        type: str
    vm_name:
        description: The name of the VM to which this IP will be assigned.
        required: false
        default: null
        type: str
    state:
        description:
            - Indicates the desired floating IP state.
            - If present, it will be created.
            - If absent, it will be deleted.
            - If unassigned, it will be unassigned from specific VM.
        default: present
        type: str
        choices: [ present, absent, unassign ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new floating IP only
  merizrizal.idcloudhost.floating_ip:
    api_key: "{{ your_api_key }}"
    location: jkt01
    name: my_floating_ip_addr01
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Create new floating IP and assign to specific VM
  merizrizal.idcloudhost.floating_ip:
    api_key: "{{ your_api_key }}"
    location: jkt01
    name: my_floating_ip_addr01
    vm_name: my_ubuntu_vm01
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Unassign floating IP
  merizrizal.idcloudhost.floating_ip:
    api_key: "{{ your_api_key }}"
    location: jkt01
    name: my_floating_ip_addr01
    state: unassign

- name: Delete floating IP
  merizrizal.idcloudhost.floating_ip:
    api_key: "{{ your_api_key }}"
    location: jkt01
    name: my_floating_ip_addr01
    state: absent
'''

RETURN = r'''
uuid:
    description: UUID of the managed floating IP.
    type: str
    returned: success
name:
    description: Name of the managed floating IP.
    type: str
    returned: success
public_ipv4:
    description: Public IPv4 address of the managed floating IP.
    type: str
    returned: success
vm_name:
    description: The name of the VM to which this IP is assigned.
    type: str
    returned: success
assigned_to_vm_uuid:
    description: The uuid of the VM to which this IP is assigned.
    type: str
    returned: success
private_ipv4_address:
    description: The address of private IPv4 to which this IP is assigned.
    type: str
    returned: success
enabled:
    description: The status of the floating IP.
    type: bool
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.merizrizal.idcloudhost.plugins.module_utils.base import \
    Base

requests = None


class FloatingIp(Base):
    def __init__(self):
        super().__init__()
        self._endpoint_url = 'network/ip_addresses'

    def main(self):
        global requests
        requests = self._ensure_requests()

        argument_spec = dict(
            api_key=dict(type='str', required=True, no_log=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            name=dict(type='str', required=True),
            vm_name=dict(type='str', default=None),
            state=dict(type='str', default='present', choices=['absent', 'present', 'unassign'])
        )

        self._module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self._name = self._module.params['name']
        self._api_key = self._module.params['api_key']
        self._location = self._module.params['location']
        self._state = self._module.params['state']
        vm_name = self._module.params['vm_name']

        floating_ip = self._get_public_ipv4(name=self._name)

        vm = dict()
        if vm_name is not None:
            vm = self._get_vm(name=vm_name)
            if 'uuid' not in vm:
                self._module.fail_json(msg='Failed to create the floating IP. The VM name is provided, but no VM was found.')

        if self._state == 'present':
            if 'uuid' in floating_ip:
                floating_ip.update(
                    vm_name='' if vm_name is None else vm_name,
                    changed=False
                )

                if 'uuid' in vm and floating_ip['assigned_to_vm_uuid'] == '':
                    data_response = self._assign_to_vm(floating_ip['public_ipv4'], vm['uuid'])
                    data_response = self._update_assigned_floating_ip(data_response, vm['name'])

                    floating_ip.update(
                        **data_response,
                        changed=True
                    )
            else:
                self._create_floating_ip(vm)
        elif self._state == 'absent':
            if 'uuid' in floating_ip:
                self._delete_public_ipv4(floating_ip['public_ipv4'])
                floating_ip.update(changed=True)
            else:
                floating_ip.update(changed=False)
        elif self._state == 'unassign':
            if 'uuid' in floating_ip:
                data_response = self._unassign_from_vm(floating_ip['public_ipv4'])
                data_response = self._update_assigned_floating_ip(data_response, '')

                floating_ip.update(
                    **data_response,
                    changed=floating_ip['assigned_to_vm_uuid'] != ''
                )
            else:
                floating_ip.update(changed=False)

        self._module.exit_json(**floating_ip)

    def _create_floating_ip(self, vm):
        url, url_headers = self._init_url(self._endpoint_url)
        url_headers.update({'Content-Type': 'application/json'})

        form_data = dict(
            name=self._name
        )

        response = requests.request('POST', url, headers=url_headers, json=form_data, timeout=360)
        data = response.json()

        if 'uuid' not in data:
            result = dict(
                error=data
            )

            self._module.fail_json(msg='Failed to create the floating IP.', **result)
        else:
            result = dict(
                uuid=data['uuid'],
                name=data['name'],
                public_ipv4=data['address'],
                vm_name='',
                assigned_to_vm_uuid='',
                private_ipv4_address='',
                enabled=data['enabled'],
                changed=True
            )

            data_response = dict()
            if 'uuid' in vm:
                data_response = self._assign_to_vm(data['address'], vm['uuid'])

            data_response = self._update_assigned_floating_ip(data_response, vm['name'])
            result.update(**data_response)

            self._module.exit_json(**result)

    def _assign_to_vm(self, ipv4_address, vm_uuid) -> dict:
        url, url_headers = self._init_url(f'{self._endpoint_url}/{ipv4_address}/assign')
        url_headers.update({'Content-Type': 'application/json'})

        form_data = dict(
            vm_uuid=vm_uuid
        )

        response = requests.request('POST', url, headers=url_headers, json=form_data, timeout=360)
        data = response.json()

        if 'uuid' in data:
            return data

        return dict(
            msg='Failed to assign the floating IP into the selected VM.',
            error=data
        )

    def _unassign_from_vm(self, ipv4_address) -> dict:
        url, url_headers = self._init_url(f'{self._endpoint_url}/{ipv4_address}/unassign')

        response = requests.request('POST', url, headers=url_headers, timeout=360)
        data = response.json()

        if 'uuid' in data:
            result = dict(**data)
            result.update(
                assigned_to='',
                assigned_to_private_ip=''
            )

            return result

        return dict(
            msg='Failed to unassign the floating IP from the selected VM.',
            error=data
        )

    def _update_assigned_floating_ip(self, floating_ip, vm_name) -> dict:
        result = dict()

        if 'uuid' in floating_ip:
            result.update(
                vm_name=vm_name,
                assigned_to_vm_uuid=floating_ip['assigned_to'],
                private_ipv4_address=floating_ip['assigned_to_private_ip']
            )
        elif 'msg' in floating_ip:
            self._module.fail_json(**floating_ip)

        return result


if __name__ == '__main__':
    FloatingIp().main()
