#!/usr/bin/env python

import phpypam
import json
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

from phpypam import PHPyPAMEntityNotFoundException


if __name__ == '__main__':
    pi = phpypam.api(
        url=server['url'],
        app_id=server['app_id'],
        username=server['username'],
        password=server['password'],
        ssl_verify=True
    )

    cidr = '10.0.0.0/24'

    try:
        entity = pi.get_entity(controller='subnets', controller_path='cidr/' + cidr)
        print("""Subnet with cidr '{0}' found:\nResult:\n{1}""".format(cidr, json.dumps(entity, indent=2, sort_keys=True)))
    except PHPyPAMEntityNotFoundException:
        print("Subnet with cidr '{0}' not found.".format(cidr))
