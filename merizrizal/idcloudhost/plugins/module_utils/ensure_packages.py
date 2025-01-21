# -*- coding: utf-8 -*-
# Copyright (c) 2025, Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)
from ansible.module_utils.basic import AnsibleModule


def ensure_requests(module: AnsibleModule):
    try:
        import requests
        HAS_REQUESTS = True
    except ImportError:
        HAS_REQUESTS = False

    if HAS_REQUESTS:
        return requests

    module.fail_json(
        msg='Could not import the requests Python module',
        results=[]
    )
