#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_network
short_description: Create VPC network
version_added: "1.0.0"

description: Create an VPC network to be used by VM resources

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    name:
        description: Name of network that will be created
        required: true
        type: str

author:
    - Mei Rizal (merizrizal) <meriz.rizal@gmail.com>
'''


EXAMPLES = r'''
- name: Create new VPC network
  merizrizal.idcloudhost.create_network:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    name: my_vpc_network_01
'''

RETURN = r'''
uuid:
    description: UUID of the created network.
    type: str
    returned: always
name:
    description: Name of the created network.
    type: str
    returned: always
subnet:
    description: Subnet of the created network.
    type: str
    returned: always
is_default:
    description: Show if the created network set as default or not.
    type: bool
    returned: always
'''


import requests
from ansible.module_utils.basic import AnsibleModule


class CreateNetWork():
    def __init__(self):
        self.base_url = 'https://api.idcloudhost.com/v1/network/network'
        self.name = ''
        self.api_key = ''

    def main(self):
        argument_spec = dict(
            api_key=dict(type='str', required=True),
            name=dict(type='str', required=True)
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self.name = module.params['name']
        self.api_key = module.params['api_key']

        url = f'{self.base_url}?name={self.name}'
        url_headers = dict(
            apikey=self.api_key
        )

        response = requests.request('POST', url, headers=url_headers, timeout=60)
        data = response.json()
        result = dict(
            uuid=data['uuid'],
            name=data['name'],
            subnet=data['subnet'],
            is_default=data['is_default'],
        )

        module.exit_json(**result)


if __name__ == '__main__':
    CreateNetWork().main()

