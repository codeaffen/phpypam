"""Tests to check funtionallity of section handling."""
import phpypam
import pytest
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

from phpypam import PHPyPAMEntityNotFoundException


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


def test_create_section():
    """Test to create a new section.

    Create a section if it doesn't exists
    """
    try:
        entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    except PHPyPAMEntityNotFoundException:
        print('create entity')
        entity = pi.create_entity(controller='sections', data=my_section)
        entity = pi.get_entity(controller='sections', controller_path=my_section['name'])

    assert entity is not None


def test_update_section():
    """Test to update an existing section.

    Update one field of an existing section.
    """
    my_section['description'] = 'new description'

    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    pi.update_entity(controller='sections', controller_path=entity['id'], data=my_section)
    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])

    assert entity['description'] == my_section['description']


# @ pytest.mark.xpass(raises=PHPyPAMEntityNotFoundException)
def test_delete_section():
    """Test to delete an existing section.

    Delete one field of an existing section.
    """
    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    pi.delete_entity(controller='sections', controller_path=entity['id'])
    entity_kwargs = dict(controller='sections', controller_path=my_section['name'])
    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **entity_kwargs)
