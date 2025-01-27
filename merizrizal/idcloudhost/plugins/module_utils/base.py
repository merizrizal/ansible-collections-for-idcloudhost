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

        global requests
        requests = self._ensure_requests()
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

    def _get_public_ipv4(self, vm_uuid=None, private_ipv4=None) -> dict:
        url, url_headers = self._init_url('network/ip_addresses')

        global requests
        requests = self._ensure_requests()
        response = requests.request('GET', url, headers=url_headers, timeout=360)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for value in data:
                is_found = value['assigned_to_private_ip'] == private_ipv4
                is_found = is_found or value['assigned_to'] == vm_uuid

                if is_found:
                    result = dict(
                        uuid=value['uuid'],
                        public_ipv4=value['address'],
                        enabled=value['enabled']
                    )

                    return result

            return dict()
