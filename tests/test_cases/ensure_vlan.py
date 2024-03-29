"""Tests to check funtionallity of vlan handling."""
import pytest
import yaml

from phpypam import PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

my_vlan = dict(
    name='my vlan',
    number='1337',
)


def test_create_vlan(pi):
    """Test to create a new vlan.

    Create a vlan if it doesn't exists
    """
    try:
        entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    except PHPyPAMEntityNotFoundException:
        entity = pi.create_entity(controller='vlan', data=my_vlan)
        entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})

    assert entity is not None


def test_update_vlan(pi):
    """Test to update an existing vlan.

    Update one field of an existing vlan
    """
    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})

    my_vlan.update({
        'vlanId': entity[0]['vlanId'],
        'description': 'description added',
    })

    pi.update_entity(controller='vlan', controller_path=entity[0]['vlanId'], data=my_vlan)
    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})

    assert entity[0]['description'] == my_vlan['description']


def test_delete_vlan(pi):
    """Test to delete an existing vlan.

    Delete vlan which we created before
    """
    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    pi.delete_entity(controller='vlan', controller_path=entity[0]['vlanId'])
    delete_kwargs = dict(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **delete_kwargs)
