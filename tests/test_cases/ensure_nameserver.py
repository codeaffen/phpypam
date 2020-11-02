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

my_nameserver = dict(
    name='my dns',
    namesrv1='127.0.01',
    permissions=1,
)


def test_create_nameserver():
    """Test to create a new nameserver

    Create a nameserver if it doesn't exists
    """
    try:
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    except PHPyPAMEntityNotFoundException:
        entity = pi.create_entity(controller='tools/nameservers', data=my_nameserver)
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    assert entity is not None


def test_update_nameserver():
    """Test to update an existing nameserver.

    Update one field of an existing nameserver
    """
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    my_nameserver.update({'description': 'description added'})

    pi.update_entity(controller='tools/nameservers', controller_path=entity[0]['id'], data=my_nameserver)
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    assert entity[0]['description'] == my_nameserver['description']


def test_delete_nameserver():
    """Test to delete an existing nameserver.

    Delete the nameserver which we created before
    """
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    pi.delete_entity(controller='tools/nameservers', controller_path=entity[0]['id'])
    delete_kwargs = dict(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **delete_kwargs)
