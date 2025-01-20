#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: get_public_ip
short_description: Get a public IPv4 address
version_added: "1.0.0"

description: Get a public IPv4 address using the selected private IPv4 address or using the selected VM

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    location:
        description: The location name where the network will be selected.
        required: true
        type: str
        choices: [ jkt01, jkt02, jkt03, sgp01 ]
    private_ipv4:
        description: Look up the public IPv4 address using this private IPv4 address.
        required: false
        type: str
    vm_uuid:
        description: Look up the public IPv4 address using this VM UUID.
        required: false
        type: str

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Get public IPv4 address from selected private_ipv4
  merizrizal.idcloudhost.get_public_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    private_ipv4: 10.51.111.211

- name: Get public IPv4 address from selected vm_uuid
  merizrizal.idcloudhost.get_public_ip:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    vm_uuid: 88e5a11b-9c89-4986-99c7-90d43499317c
'''

RETURN = r'''
uuid:
    description: UUID of the floating IP.
    type: str
    returned: success
public_ipv4:
    description: Public IPv4 address.
    type: str
    returned: success
enabled:
    description: Status.
    type: bool
    returned: success
assigned_to:
    description: On which VM this public IPv4 is assigned.
    type: bool
    returned: success, when private_ipv4 is selected
assigned_to_private_ip:
    description: On which private Ipv4 this public IPv4 is assigned.
    type: bool
    returned: success, when vm_uuid is selected
'''

import requests
from ansible.module_utils.basic import AnsibleModule


class GetPublicIP():
    def __init__(self):
        self.base_url = 'https://api.idcloudhost.com/v1'
        self.endpoint_url = 'network/ip_addresses'
        self.api_key = ''
        self.location = ''
        self.private_ipv4 = ''
        self.vm_uuid = ''

    def main(self):
        argument_spec = dict(
            api_key=dict(type='str', required=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            private_ipv4=dict(type='str', required=False),
            vm_uuid=dict(type='str', required=False)
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_one_of=[
                ('private_ipv4', 'vm_uuid'),
            ],
            mutually_exclusive=[
                ('private_ipv4', 'vm_uuid'),
            ]
        )

        self.api_key = module.params['api_key']
        self.location = module.params['location']
        self.private_ipv4 = module.params['private_ipv4']
        self.vm_uuid = module.params['vm_uuid']

        url = f'{self.base_url}/{self.location}/{self.endpoint_url}'
        url_headers = dict(
            apikey=self.api_key
        )

        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if not isinstance(data, list) or (isinstance(data, list) and len(data) <= 0):
            result = dict(
                error=data
            )

            module.fail_json(msg='Get public IPv4 fail', **result)
        else:
            result = dict(
                error='Public IPv4 address is not found'
            )

            for value in data:
                is_found = value['assigned_to_private_ip'] == self.private_ipv4
                is_found = is_found or value['assigned_to'] == self.vm_uuid

                if is_found:
                    result = dict(
                        uuid=value['uuid'],
                        public_ipv4=value['address'],
                        enabled=value['enabled']
                    )

                    if self.private_ipv4:
                        result.update(assigned_to=value['assigned_to'])
                    elif self.vm_uuid:
                        result.update(assigned_to_private_ip=value['assigned_to_private_ip'])

                    module.exit_json(**result)

            module.fail_json(msg='Get public IPv4 fail', **result)


if __name__ == '__main__':
    GetPublicIP().main()
