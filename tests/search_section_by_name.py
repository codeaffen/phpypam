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

    search_params = [
        {'filter_by': 'name', 'filter_value': 'non_existing_section'},
        {'filter_by': 'name', 'filter_value': 'IPv6', 'filter_match': 'full'},
    ]

    for search in search_params:
        try:
            entity = pi.get_entity(controller='sections', params=search)
            print("""Entity with name '{0}' found:\nResult:\n{1}""".format(search['filter_value'], json.dumps(entity, indent=2, sort_keys=True)))
        except PHPyPAMEntityNotFoundException:
            print("Entity with name '{0}' not found.".format(search['filter_value']))
