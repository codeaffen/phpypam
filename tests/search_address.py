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

    addr = '10.10.0.4'

    try:
        entity = pi.get_entity(controller='addresses', controller_path='search/' + addr)
        print("""Address '{0}' found:\nResult:\n{1}""".format(addr, json.dumps(entity, indent=2, sort_keys=True)))
    except PHPyPAMEntityNotFoundException:
        print("Address '{0}' not found.".format(addr))
