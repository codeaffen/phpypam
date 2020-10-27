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

    my_vlan = dict(
        name='my vlan',
        number='1337',
    )

    try:
        entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': 'my vlan'})
    except PHPyPAMEntityNotFoundException:
        print('create entity')
        entity = pi.create_entity(controller='vlan', data=my_vlan)

    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': 'my vlan'})
    print(json.dumps(entity, indent=4, sort_keys=True))

    my_vlan = {
        'vlanId': entity[0]['vlanId'],
        'name': 'my vlan',
        'description': 'description added',
    }

    print('update entity')
    pi.update_entity(controller='vlan', controller_path=entity[0]['vlanId'], data=my_vlan)

    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': 'my vlan'})
    print(json.dumps(entity, indent=4, sort_keys=True))

    print('delete entity')
    pi.delete_entity(controller='vlan', controller_path=entity[0]['vlanId'])
