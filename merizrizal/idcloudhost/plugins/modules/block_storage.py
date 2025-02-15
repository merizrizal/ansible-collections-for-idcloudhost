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
    uuid:
        description:
            - UUID of a block storage that will be managed.
            - This is required if state is set to absent, attach or detach.
        required: false
        default: null
        type: str
    vm_name:
        description:
            - Name of the VM to which this block storage is attached.
            - This is required if state is set to attach or detach.
            - If state is set to present then the block storage will be attached to the selected VM
        required: false
        default: null
        type: str
    size:
        description:
            - Size of the block storage in GB.
            - This is required if state is set to present.
        required: false
        default: null
        type: int
    state:
        description:
            - Indicates the desired block storage state.
            - If present, it will be created.
            - If absent, it will be deleted.
            - If attach, it will be attached to the specific VM.
            - If detach, it will be detached from the specific VM.
        default: present
        type: str
        choices: [ present, absent, attach, detach ]

author:
    - Mei Rizal (@merizrizal) <meriz.rizal@gmail.com>
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''
