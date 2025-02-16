#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: block_storage
short_description: Manage VM block storage a.k.a disks
version_added: "1.0.0"

description: Manage block storage from a selected location.

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
        description:
            - Name of a block storage that will be managed. It is usually named vdb, vdc, vdd, vde, and so on
            - This is required if state is set to absent
        default: null
        type: str
    vm_name:
        description: Name of the VM to which this block storage is attached.
        required: true
        type: str
    size:
        description:
            - Size of the block storage in GB.
            - This is required if state is set to present.
        default: null
        type: int
    state:
        description:
            - Indicates the desired block storage state.
            - If present, it will be created and attached to the selected VM.
            - If absent, it will be detached and deleted by selecting the disk name which is available on the VM.
        default: present
        type: str
        choices: [ present, absent ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
- name: Create block storage
  merizrizal.idcloudhost.block_storage:
    api_key: "{{ your_api_key }}"
    location: jkt01
    vm_name: my_ubuntu_vm01
    size: 10
    # Since the default value of state is set to present, we may exclude the state below
    state: present

- name: Delete block storage
  merizrizal.idcloudhost.block_storage:
    api_key: "{{ your_api_key }}"
    location: jkt01
    name: vdb
    vm_name: my_ubuntu_vm01
    state: absent
'''

RETURN = r'''
uuid:
    description: UUID of the managed block storage.
    type: str
    returned: success
name:
    description: Name of the managed block storage. It is usually named vdb, vdc, vdd, vde, and so on.
    type: str
    returned: success
size:
    description: Size of the block storage in GB.
    type: int
    returned: success
vm_name:
    description: Name of the VM to which this block storage is attached.
    type: str
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.merizrizal.idcloudhost.plugins.module_utils.base import \
    Base

requests = None


class BlockStorage(Base):
    def __init__(self):
        super().__init__()
        self._endpoint_url = 'user-resource/vm/storage'

    def main(self):
        global requests
        requests = self._ensure_requests()

        argument_spec = dict(
            api_key=dict(type='str', required=True, no_log=True),
            location=dict(type='str', required=True, choices=['jkt01', 'jkt02', 'jkt03', 'sgp01']),
            name=dict(type='str', default=None),
            vm_name=dict(type='str', required=True),
            size=dict(type='int', default=None),
            state=dict(type='str', default='present', choices=['absent', 'present'])
        )

        self._module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True,
            required_if=[
                ('state', 'absent', ('name',)),
                ('state', 'present', ('size',))
            ]
        )

        self._api_key = self._module.params['api_key']
        self._location = self._module.params['location']
        self._name = self._module.params['name']
        self._size = self._module.params['size']
        self._state = self._module.params['state']
        vm_name = self._module.params['vm_name']

        vm = dict()
        if vm_name is not None:
            vm = self._get_vm(name=vm_name, include_storage=True)
            if 'uuid' not in vm:
                self._module.fail_json(msg='Failed to create the block storage. The VM name is provided, but no VM was found.')

        if self._state == 'present':
            self._create_block_storage(vm)
        elif self._state == 'absent':
            self._delete_block_storage(vm)

    def _create_block_storage(self, vm):
        url, url_headers = self._init_url()
        url_headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

        form_data = dict(
            uuid=vm['uuid'],
            size_gb=self._size
        )

        response = requests.request('POST', url, headers=url_headers, data=form_data, timeout=360)
        data = response.json()

        if 'uuid' not in data:
            result = dict(
                error=data
            )

            self._module.fail_json(msg='Failed to create the block storage.', **result)
        else:
            result = dict(
                uuid=data['uuid'],
                name=data['name'],
                size=data['size'],
                vm_name=vm['name'],
                changed=True
            )

            self._module.exit_json(**result)

    def _delete_block_storage(self, vm):
        disk = self._get_disk_from_vm(vm)
        if 'uuid' not in disk:
            self._module.fail_json(msg='Failed to create the block storage. The block storage name is provided, but no disk was found.')

        url, url_headers = self._init_url()
        url_headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

        disk_uuid = disk['uuid']
        form_data = dict(
            storage_uuid=disk_uuid,
            uuid=vm['uuid']
        )

        response = requests.request('DELETE', url, headers=url_headers, data=form_data, timeout=360)
        data = response.json()

        if 'success' not in data:
            result = dict(
                error=data
            )

            self._module.fail_json(msg='Failed to delete the block storage.', **result)
        else:
            url, url_headers = self._init_url(f'storage/disks/{disk_uuid}')
            response = requests.request('DELETE', url, headers=url_headers, data=form_data, timeout=360)
            if response.status_code != 204:
                result = dict(
                    error='There was a problem with the request when deleting the block storage.'
                )

                self._module.fail_json(msg='Failed to delete the block storage.', **result)

            result = dict(changed=True)

            self._module.exit_json(**result)

    def _get_disk_from_vm(self, vm) -> dict:
        for storage in vm['storage_list']:
            if storage['name'] == self._name:
                return storage

        return dict()


if __name__ == '__main__':
    BlockStorage().main()
