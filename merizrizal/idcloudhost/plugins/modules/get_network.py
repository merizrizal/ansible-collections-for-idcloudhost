#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: get_network
short_description: Get existing VPC network
version_added: "1.0.0"

description: Get a default VPC network resource from selected location

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

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Get VPC network
  merizrizal.idcloudhost.get_network:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
'''

RETURN = r'''
uuid:
    description: UUID of the network.
    type: str
    returned: success
name:
    description: Name of the network.
    type: str
    returned: success
subnet:
    description: Subnet of the network.
    type: str
    returned: success
'''

import requests
from ansible.module_utils.basic import AnsibleModule


class GetNetwork():
    def __init__(self):
        self.base_url = 'https://api.idcloudhost.com/v1'
        self.endpoint_url = 'network/networks'
        self.api_key = ''
        self.location = ''

    def main(self):
        argument_spec = dict(
            api_key=dict(type='str', required=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01'])
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self.api_key = module.params['api_key']
        self.location = module.params['location']

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

            module.fail_json(msg='Get network fail', **result)
        else:
            for value in data:
                if value['is_default']:
                    result = dict(
                        uuid=value['uuid'],
                        name=value['name'],
                        subnet=value['subnet']
                    )

                    module.exit_json(**result)


if __name__ == '__main__':
    GetNetwork().main()
