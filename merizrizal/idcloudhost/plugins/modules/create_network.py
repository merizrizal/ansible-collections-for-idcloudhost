#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_network
short_description: Create new VPC network
version_added: "1.0.0"

description: Create an VPC network into selected location to be used by VM resources

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    name:
        description: Name of network that will be created.
        required: true
        type: str
    location:
        description: The location name of the network to which this network will be assigned.
        required: true
        type: str
        choices: [ jkt01, jkt02, jkt03, sgp01 ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new VPC network
  merizrizal.idcloudhost.create_network:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    name: my_vpc_network_01
    location: jkt01
'''

RETURN = r'''
uuid:
    description: UUID of the created network.
    type: str
    returned: success
name:
    description: Name of the created network.
    type: str
    returned: success
subnet:
    description: Subnet of the created network.
    type: str
    returned: success
is_default:
    description: Show if the created network set as default or not.
    type: bool
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.merizrizal.idcloudhost.plugins.module_utils.ensure_packages import \
    ensure_requests

requests = None


class CreateNetwork():
    def __init__(self):
        self.base_url = 'https://api.idcloudhost.com/v1'
        self.endpoint_url = 'network/network'
        self.api_key = ''
        self.name = ''
        self.location = ''

    def main(self):
        argument_spec = dict(
            api_key=dict(type='str', required=True, no_log=True),
            name=dict(type='str', required=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01'])
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        requests = ensure_requests(module)

        self.name = module.params['name']
        self.api_key = module.params['api_key']
        self.location = module.params['location']

        url = f'{self.base_url}/{self.location}/{self.endpoint_url}?name={self.name}'
        url_headers = dict(
            apikey=self.api_key
        )

        response = requests.request('POST', url, headers=url_headers, timeout=360)
        data = response.json()

        if 'uuid' not in data:
            result = dict(
                error=data
            )

            module.fail_json(msg='Create network fail', **result)
        else:
            result = dict(
                uuid=data['uuid'],
                name=data['name'],
                subnet=data['subnet'],
                is_default=data['is_default'],
            )

            module.exit_json(**result)


if __name__ == '__main__':
    CreateNetwork().main()
