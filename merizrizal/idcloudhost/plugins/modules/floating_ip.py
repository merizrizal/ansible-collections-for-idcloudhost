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
        description: The location name of the network to which this network is assigned.
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
        type: str
    state:
        description:
            - Indicates the desired floating IP state.
            - If present, it will be created.
            - If absent, it will be deleted.
            - If unassigned, it will be unassigned from specific VM.
        default: present
        type: str
        choices: [ present, absent, unassigned ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new floating IP only
  merizrizal.idcloudhost.floating_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    name: my_floating_ip_addr01
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Create new floating IP and assign to specific VM
  merizrizal.idcloudhost.floating_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    name: my_floating_ip_addr01
    vm_name: my_ubuntu_vm01
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Unassign floating IP
  merizrizal.idcloudhost.floating_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    name: my_floating_ip_addr01
    state: unassign

- name: Delete floating IP
  merizrizal.idcloudhost.floating_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
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
ipv4_address:
    description: Public IPv4 address of the managed floating IP.
    type: str
    returned: success
vm_name:
    description: The name of the VM to which this IP is assigned.
    type: str
    returned: success
private_ipv4_address:
    description: The address of private IPv4 to which this IP is assigned.
    type: str
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
            vm_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['absent', 'present', 'unassigned'])
        )

        self._module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self._name = self._module.params['name']
        self._api_key = self._module.params['api_key']
        self._location = self._module.params['location']
        self._state = self._module.params['state']

        floating_ip = self._get_public_ipv4(name=self._name)

        if self._state == 'present':
            if 'uuid' in floating_ip:
                floating_ip.update(changed=False)
            else:
                self._create_floating_ip()
        elif self._state == 'absent':
            if 'uuid' in floating_ip:
                self._delete_public_ipv4(floating_ip['public_ipv4'])
                floating_ip.update(changed=True)
            else:
                floating_ip.update(changed=False)

        self._module.exit_json(**floating_ip)

    def _create_floating_ip(self):
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
                ipv4_address=data['address'],
                vm_name='',
                private_ipv4_address='',
                changed=True
            )

            self._module.exit_json(**result)


if __name__ == '__main__':
    FloatingIp().main()
