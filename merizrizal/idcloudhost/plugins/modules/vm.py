#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: vm
short_description: Manage VM resource
version_added: "1.0.0"

description: Manage VM resource from selected location

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
    network_name:
        description:
            - Name of the network that will be attached to the VM.
            - This is required if state is set to present.
        type: str
    name:
        description: Informative name, it will also be used to generate a suitable hostname for the VM (if applicable).
        required: true
        type: str
    os_name:
        description:
            - Operating system that will be installed into the VM.
            - This is required if state is set to present.
        type: str
        choices: [ almalinux, bsd, centos, cloudlinux, debian, fedora, opensuse, oracle, rhel, rocky, ubuntu, vzlinux, windows  ]
    os_version:
        description:
            - The operating system version.
            - This is required if state is set to present.
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
        type: str
        choices: [ '8.x', '8.4', '9.x', '32', '24.04-lts', 'linux_8.4', 'server_7.9', '11', '2019', '34', '7.9',
            'freebsd_12.2', '15.3', 'server_8.4', '12', '21.04', '36', '22.04-lts', '20.04-lts' ]
    disks:
        description:
            - Size of main storage in GB.
            - This is required if state is set to present.
        type: int
    vcpu:
        description:
            - Numbers of CPU.
            - This is required if state is set to present.
        type: int
    ram:
        description:
            - Size of RAM in MB.
            - This is required if state is set to present.
        type: int
    username:
        description:
            - A user account will be created with this username, it can be used to log in to the VM.
            - Can contain ASCII letters, digits, underscores and hyphens. Must start with a letter or underscore. Maximum length is 25 characters.
            - This is required if state is set to present.
        type: str
    password:
        description:
            - Password for the user. Must contain at least one lowercase and one uppercase ASCII letter (a-z, A-Z) and at least one digit (0-9).
            - Minimum length is 8 characters.
            - This is required if state is set to present.
        type: str
    remove_public_ipv4:
        description:
            - Flag to remove public IPv4 address.
            - This is required if state is set to absent.
        default: null
        type: bool
    state:
        description:
            - Indicates the desired VM state.
            - If present, it will be created.
            - If absent, it will be deleted.
        default: present
        type: str
        choices: [ present, absent ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create new VM
  merizrizal.idcloudhost.vm:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    network_name: my_network_jkt01
    name: my_ubuntu_vm01
    os_name: ubuntu
    os_version: 24.04-lts
    disks: 20
    vcpu: 2
    ram: 2048
    username: my_admin_user
    password: My4adminpass
    # Since the default value of state is set to present, we can exclude it
    state: present

- name: Delete VM
  merizrizal.idcloudhost.vm:
    api_key: 2bnQkD6yOb7OkSwVCBXJSg1AHpfd99oY
    location: jkt01
    name: my_ubuntu_vm01
    remove_public_ipv4: true
    state: absent
'''

RETURN = r'''
uuid:
    description: UUID of the created VM.
    type: str
    returned: success
name:
    description: Informative VM name.
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
public_ipv4:
    description: Public IPv4 of the created VM.
    type: str
    returned: success
billing_account:
    description: The selected billing account that will be paying for the created VM.
    type: str
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.merizrizal.idcloudhost.plugins.module_utils.base import \
    Base

requests = None


class Vm(Base):
    def __init__(self):
        super().__init__()
        self._endpoint_url = 'user-resource/vm'

    def main(self):
        global requests
        requests = self._ensure_requests()

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
            api_key=dict(type='str', required=True, no_log=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            network_name=dict(type='str'),
            name=dict(type='str', required=True),
            os_name=dict(type='str', choices=all_os_choices),
            os_version=dict(type='str', choices=all_os_version_choices),
            disks=dict(type='int'),
            vcpu=dict(type='int'),
            ram=dict(type='int'),
            username=dict(type='str'),
            password=dict(type='str', no_log=True),
            remove_public_ipv4=dict(type='bool', default=None),
            state=dict(type='str', default='present', choices=['absent', 'present'])
        )

        self._module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=[
                ('state', 'present', (
                    'network_name', 'os_name', 'os_version',
                    'disks', 'vcpu', 'ram', 'username', 'password')),
                ('state', 'absent', ('remove_public_ipv4',))
            ]
        )

        self._api_key = self._module.params['api_key']
        self._location = self._module.params['location']
        self._name = self._module.params['name']
        self._state = self._module.params['state']

        vm = self._get_vm()
        if self._state == 'present':
            if 'uuid' in vm:
                vm.update(changed=False)
            else:
                network = self._get_network()
                self._create_vm(os_version_choices, network)
        elif self._state == 'absent':
            if 'uuid' in vm:
                vm = self._delete_vm(vm)

                if self._module.params['remove_public_ipv4']:
                    self._delete_public_ipv4(vm['public_ipv4'])
            else:
                vm.update(changed=False)

        self._module.exit_json(**vm)

    def _get_vm(self) -> dict:
        url = f'{self._base_url}/{self._location}/user-resource/vm/list'
        url_headers = dict(
            apikey=self._api_key
        )

        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for value in data:
                if value['name'] == self._name:
                    return self._construct_vm_data(value)

        return dict()

    def _construct_vm_data(self, data) -> dict:
        floating_ip = self._get_public_ipv4(data['uuid'], data['private_ipv4'])
        public_ipv4 = '' if 'public_ipv4' not in floating_ip else floating_ip['public_ipv4']

        vm = dict(
            uuid=data['uuid'],
            name=data['name'],
            hostname=data['hostname'],
            private_ipv4=data['private_ipv4'],
            public_ipv4=public_ipv4,
            billing_account=data['billing_account'],
            changed=True
        )

        return vm

    def _get_network(self) -> dict:
        network = self._get_existing_network(self._module.params['network_name'])

        if 'uuid' not in network:
            result = dict(
                error='The selected network is not found.'
            )

            self._module.fail_json(msg='Create VM fail.', **result)

        return network

    def _create_vm(self, os_version_choices, network):
        os_name = self._module.params['os_name']
        os_version = self._module.params['os_version']

        if os_version not in os_version_choices[os_name]:
            result = dict(
                error=f'Selected os_name is {os_name} then os_version must be one of {os_version_choices[os_name]}, got {os_version}'
            )

            self._module.fail_json(msg='Create VM fail', **result)

        url = f'{self._base_url}/{self._location}/{self._endpoint_url}'
        url_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': self._api_key
        }

        form_data = dict(
            network_uuid=network['uuid'],
            name=self._name,
            os_name=os_name,
            os_version=os_version,
            disks=self._module.params['disks'],
            vcpu=self._module.params['vcpu'],
            ram=self._module.params['ram'],
            username=self._module.params['username'],
            password=self._module.params['password'],
        )

        response = requests.request('POST', url, headers=url_headers, data=form_data, timeout=360)
        data = response.json()

        if 'uuid' not in data:
            result = dict(
                error=data
            )

            self._module.fail_json(msg='Create VM fail', **data)
        else:
            result = self._construct_vm_data(data)

            self._module.exit_json(**result)

    def _delete_vm(self, vm) -> dict:
        if 'uuid' in vm:
            url = f'{self._base_url}/{self._location}/{self._endpoint_url}'
            url_headers = dict(
                apikey=self._api_key
            )

            form_data = dict(
                uuid=vm['uuid']
            )

            response = requests.request('DELETE', url, headers=url_headers, data=form_data, timeout=360)

            if response.status_code == 200:
                vm.update(changed=True)
            else:
                result = dict(
                    error='There was a problem with the request.'
                )

                self._module.fail_json(msg='Delete VM fail', **result)
        else:
            vm.update(changed=False)

        return vm

    def _delete_public_ipv4(self, public_ipv4):
        url = f'{self._base_url}/{self._location}/network/ip_addresses/{public_ipv4}'
        url_headers = dict(
            apikey=self._api_key
        )

        response = requests.request('DELETE', url, headers=url_headers, timeout=360)

        if response.status_code != 200:
            result = dict(
                error='There was a problem with the request when deleting the public IPv4 address.'
            )

            self._module.fail_json(msg='Delete VM fail', **result)


if __name__ == '__main__':
    Vm().main()
