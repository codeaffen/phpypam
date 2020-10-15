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

    my_section = dict(
        name='foobar',
        description='new section',
        permissions='{"3":"1","2":"2"}'
    )
    try:
        entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    except PHPyPAMEntityNotFoundException:
        print('create entity')
        entity = pi.create_entity(controller='sections', data=my_section)
        entity = pi.get_entity(controller='sections', controller_path=my_section['name'])

    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    print(json.dumps(entity, indent=4, sort_keys=True))

    my_section['description'] = 'new description'

    print('update entity')
    pi.update_entity(controller='sections', controller_path=entity['id'], data=my_section)

    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    print(json.dumps(entity, indent=4, sort_keys=True))

    print('delete entity')
    pi.delete_entity(controller='sections', controller_path=entity['id'])
