# -*- coding: utf-8 -*-
# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)
from ansible.module_utils.basic import AnsibleModule

requests = None


class Base(object):
    def __init__(self):
        self._base_url = 'https://api.idcloudhost.com/v1'
        self._endpoint_url = ''
        self._api_key = ''
        self._name = ''
        self._location = ''
        self._state = 'present'

        self._module: AnsibleModule = None

        global requests
        requests = self._ensure_requests()

    def _ensure_requests(self):
        try:
            import requests
            HAS_REQUESTS = True
        except ImportError:
            HAS_REQUESTS = False

        if HAS_REQUESTS:
            return requests

        if self._module:
            self._module.fail_json(
                msg='Could not import the requests Python module',
                results=[]
            )

    def _init_url(self, endpoint_url=None) -> tuple[str, dict]:
        endpoint_url_result = self._endpoint_url if endpoint_url is None else endpoint_url
        url = f'{self._base_url}/{self._location}/{endpoint_url_result}'
        url_headers = dict(
            apikey=self._api_key
        )

        return url, url_headers

    def _get_existing_network(self, name) -> dict:
        url, url_headers = self._init_url('network/networks')

        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for value in data:
                if value['name'] == name:
                    network = dict(
                        uuid=value['uuid'],
                        name=value['name'],
                        subnet=value['subnet'],
                        is_default=value['is_default']
                    )

                    return network

        return dict()

    def _get_public_ipv4(self, vm_uuid=None, private_ipv4=None, name=None) -> dict:
        url, url_headers = self._init_url('network/ip_addresses')

        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for value in data:
                is_found = 'assigned_to_private_ip' in value and value['assigned_to_private_ip'] == private_ipv4
                is_found = is_found or ('assigned_to' in value and value['assigned_to'] == vm_uuid)
                is_found = is_found or ('name' in value and value['name'] == name)

                if is_found:
                    result = dict(
                        uuid=value['uuid'],
                        name='' if 'name' not in value else value['name'],
                        public_ipv4=value['address'],
                        assigned_to_vm_uuid='' if 'assigned_to' not in value else value['assigned_to'],
                        private_ipv4_address='' if 'assigned_to_private_ip' not in value else value['assigned_to_private_ip'],
                        enabled=value['enabled']
                    )

                    return result

            return dict()

    def _delete_public_ipv4(self, public_ipv4):
        url, url_headers = self._init_url(f'network/ip_addresses/{public_ipv4}')

        response = requests.request('DELETE', url, headers=url_headers, timeout=360)

        if response.status_code != 200:
            result = dict(
                error='There was a problem with the request when deleting the public IPv4 address.'
            )

            self._module.fail_json(msg='Failed to delete the VM.', **result)

    def _get_vm(self, uuid=None, name=None, include_public_ipv4=True) -> dict:
        url, url_headers = self._init_url('user-resource/vm/list')

        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for value in data:
                if value['uuid'] == uuid or value['name'] == name:
                    return self._construct_vm_data(value, include_public_ipv4)

        return dict()

    def _construct_vm_data(self, data, include_public_ipv4=True) -> dict:
        floating_ip = dict()
        if include_public_ipv4:
            floating_ip = self._get_public_ipv4(data['uuid'], data['private_ipv4'])

        public_ipv4 = '' if 'public_ipv4' not in floating_ip else floating_ip['public_ipv4']

        disks = 0
        disk_uuid = ''
        for storage in data['storage']:
            if storage['primary']:
                disks = storage['size']
                disk_uuid = storage['uuid']
                break

        vm = dict(
            uuid=data['uuid'],
            name=data['name'],
            hostname=data['hostname'],
            disks=disks,
            disk_uuid=disk_uuid,
            vcpu=data['vcpu'],
            ram=data['memory'],
            private_ipv4=data['private_ipv4'],
            public_ipv4=public_ipv4,
            billing_account=data['billing_account'],
            status=data['status'],
            changed=False
        )

        return vm
