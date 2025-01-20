#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_vm
short_description: Create new VM resource
version_added: "1.0.0"

description: Create a new VM resource into selected location

options:
    api_key:
        description: API of idcloudhost.com uses tokens to allow access to the API.
        required: true
        type: str
    location:
        description: The location name of the network to which this network will be assigned.
        required: true
        type: str
        choices: [ jkt01, jkt02, jkt03, sgp01 ]
    network_uuid:
        description: UUID of which network that will be used. Use get_network module to get the UUID.
        required: true
        type: str
    name:
        description: Informative name, it will also be used to generate a suitable hostname for the VM (if applicable).
        required: true
        type: str
    os_name:
        description: Operating system that will be installed into the VM.
        required: true
        type: str
        choices: [ almalinux, bsd, centos, cloudlinux, debian, fedora, opensuse, oracle, rhel, rocky, ubuntu, vzlinux, windows  ]
    os_version:
        description:
            - The operating system version.
            - If almalinux [ 9.x, 8.x ]
            - If bsd [ freebsd_12.2 ]
            - If centos [ 9.x ]
            - If cloudlinux [ 8.4, 7.9 ]
            - If debian [ 11, 12 ]
            - If fedora [ 32, 34, 36 ]
            - If opensuse [ 15.3 ]
            - If oracle [ 9.x ]
            - If rhel [ server_7.9, server_8.4 ]
            - If rocky [ linux_8.4, 9.x ]
            - If ubuntu [ 20.04-lts, 21.04, 22.04-lts, 24.04-lts ]
            - If vzlinux [ 8.x ]
            - If windows [ 2019 ]
        required: true
        type: str
        choices: [ ... ]
    disks:
        description: Size of main storage in GB.
        required: true
        type: int
    vcpu:
        description: Numbers of CPU.
        required: true
        type: int
    ram:
        description: Size of RAM in MB.
        required: true
        type: int
    username:
        description:
            - A user account will be created with this username, it can be used to log in to the VM.
            - Can contain ASCII letters, digits, underscores and hyphens. Must start with a letter or underscore. Maximum length is 25 characters.
        required: true
        type: str
    password:
        description:
            - Password for the user. Must contain at least one lowercase and one uppercase ASCII letter (a-z, A-Z) and at least one digit (0-9).
            - Minimum length is 8 characters.
        required: true
        type: str

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new VM
  merizrizal.idcloudhost.create_network:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    network_uuid: "{{ get_from_get_network.uuid }}"
    name: my_ubuntu_vm01
    os_name: ubuntu
    os_version: 24.04-lts
    disks: 20
    vcpu: 2
    ram: 2048
    username: my_admin_user
    password: My4adminpass
'''

RETURN = r'''
uuid:
    description: UUID of the created VM.
    type: str
    returned: success
hostname:
    description: Machine hostname.
    type: str
    returned: success
private_ipv4:
    description: Private IPv4 of the created VM.
    type: str
    returned: success
billing_account:
    description: The selected billing account that will be paying for the created VM.
    type: str
    returned: success
'''

import requests
from ansible.module_utils.basic import AnsibleModule


class CreateVM():
    def __init__(self):
        self.base_url = 'https://api.idcloudhost.com/v1'
        self.endpoint_url = 'user-resource/vm'
        self.api_key = ''
        self.location = ''

    def main(self):
        os_version_choices = dict(
            almalinux=['9.x', '8.x'],
            bsd=['freebsd_12.2'],
            centos=['9.x'],
            cloudlinux=['8.4', '7.9'],
            debian=['11', '12'],
            fedora=['32', '34', '36'],
            opensuse=['15.3'],
            oracle=['9.x'],
            rhel=['server_7.9', 'server_8.4'],
            rocky=['linux_8.4', '9.x'],
            ubuntu=['21.04', '22.04-lts', '24.04-lts', '20.04-lts'],
            vzlinux=['8.x'],
            windows=['2019']
        )

        all_os_choices = list(os_version_choices)
        all_os_version_choices = []
        for os in os_version_choices:
            all_os_version_choices += os_version_choices[os]

        all_os_version_choices = list(set(all_os_version_choices))

        argument_spec = dict(
            api_key=dict(type='str', required=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            network_uuid=dict(type='str', required=True),
            name=dict(type='str', required=True),
            os_name=dict(type='str', required=True, choices=all_os_choices),
            os_version=dict(type='str', required=True, choices=all_os_version_choices),
            disks=dict(type='int', required=True),
            vcpu=dict(type='int', required=True),
            ram=dict(type='int', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True)
        )

        module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
        )

        self.api_key = module.params['api_key']
        self.location = module.params['location']

        os_name = module.params['os_name']
        os_version = module.params['os_version']

        if os_version not in os_version_choices[os_name]:
            result = dict(
                error=f'Selected os_name is {os_name} then os_version must be one of {os_version_choices[os_name]}, got {os_version}'
            )

            module.fail_json(msg='Create VM fail', **result)

        url = f'{self.base_url}/{self.location}/{self.endpoint_url}'
        url_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': self.api_key
        }

        form_data = dict(
            network_uuid=module.params['network_uuid'],
            name=module.params['name'],
            os_name=os_name,
            os_version=os_version,
            disks=module.params['disks'],
            vcpu=module.params['vcpu'],
            ram=module.params['ram'],
            username=module.params['username'],
            password=module.params['password'],
        )

        response = requests.request('POST', url, headers=url_headers, data=form_data, timeout=360)
        data = response.json()

        if 'uuid' not in data:
            result = dict(
                error=data
            )

            module.fail_json(msg='Create VM fail', **data)
        else:
            result = dict(
                uuid=data['uuid'],
                hostname=data['hostname'],
                private_ipv4=data['private_ipv4'],
                billing_account=data['billing_account'],
            )

            module.exit_json(**result)


if __name__ == '__main__':
    CreateVM().main()
