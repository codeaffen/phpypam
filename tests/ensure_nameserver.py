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

    my_nameserver = dict(
        name='my dns',
        namesrv1='127.0.01',
        permissions=1,
    )

    try:
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    except PHPyPAMEntityNotFoundException:
        print('create entity')
        entity = pi.create_entity(controller='tools/nameservers', data=my_nameserver)
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    print(json.dumps(entity, indent=4, sort_keys=True))

    my_nameserver.update({'description': 'description added'})

    print('update entity')
    pi.update_entity(controller='tools/nameservers', controller_path=entity[0]['id'], data=my_nameserver)

    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    print(json.dumps(entity, indent=4, sort_keys=True))

    print('delete entity')
    pi.delete_entity(controller='tools/nameservers', controller_path=entity[0]['id'])
