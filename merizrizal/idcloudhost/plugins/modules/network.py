#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: network
short_description: Manage VPC networks
version_added: "1.0.0"

description: Manage VPC networks from a selected location.

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    name:
        description: Name of network that will be managed.
        required: true
        type: str
    location:
        description: The location name of the network to which this network is assigned.
        required: true
        type: str
        choices: [ jkt01, jkt02, jkt03, sgp01 ]
    state:
        description:
            - Indicates the desired VPC network state.
            - If present, it will be created.
            - If absent, it will be deleted.
        default: present
        type: str
        choices: [ present, absent ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new VPC network
  merizrizal.idcloudhost.network:
    api_key: "{{ your_api_key }}"
    name: my_vpc_network_01
    location: jkt01
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Delete VPC network
  merizrizal.idcloudhost.network:
    api_key: "{{ your_api_key }}"
    name: my_vpc_network_01
    location: jkt01
    state: absent
'''

RETURN = r'''
uuid:
    description: UUID of the managed network.
    type: str
    returned: success
name:
    description: Name of the managed network.
    type: str
    returned: success
subnet:
    description: Subnet of the managed network.
    type: str
    returned: success
is_default:
    description: Show if the managed network is set as default or not.
    type: bool
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.merizrizal.idcloudhost.plugins.module_utils.base import \
    Base

requests = None


class Network(Base):
    def __init__(self):
        super().__init__()
        self._endpoint_url = 'network/network'

    def main(self):
        global requests
        requests = self._ensure_requests()

        argument_spec = dict(
            api_key=dict(type='str', required=True, no_log=True),
            name=dict(type='str', required=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            state=dict(type='str', default='present', choices=['absent', 'present'])
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self._name = module.params['name']
        self._api_key = module.params['api_key']
        self._location = module.params['location']
        self._state = module.params['state']

        network = self._get_existing_network(self._name)

        if self._state == 'present':
            if 'uuid' in network:
                network.update(changed=False)
            else:
                url, url_headers = self._init_url(f'{self._endpoint_url}?name={self._name}')

                response = requests.request('POST', url, headers=url_headers, timeout=360)
                data = response.json()

                if 'uuid' not in data:
                    result = dict(
                        error=data
                    )

                    module.fail_json(msg='Failed to create the VPC network.', **result)
                else:
                    network = dict(
                        uuid=data['uuid'],
                        name=data['name'],
                        subnet=data['subnet'],
                        is_default=data['is_default'],
                        changed=True
                    )
        elif self._state == 'absent':
            if 'uuid' in network:
                uuid = network['uuid']
                url, url_headers = self._init_url(f'{self._endpoint_url}/{uuid}')

                response = requests.request('DELETE', url, headers=url_headers, timeout=360)

                if response.status_code == 200:
                    network.update(changed=True)
                else:
                    result = dict(
                        error=response.json()
                    )

                    module.fail_json(msg='Failed to delete the VPC network.', **result)
            else:
                network.update(changed=False)

        module.exit_json(**network)


if __name__ == '__main__':
    Network().main()
