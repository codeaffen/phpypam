#!/usr/bin/env python

import phpypam
import json
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

if __name__ == '__main__':
    pi = phpypam.api(
        url=server['url'],
        app_id=server['app_id'],
        username=server['username'],
        password=server['password'],
        ssl_verify=True
    )

    controllers = pi.controllers()
    print(controllers)
