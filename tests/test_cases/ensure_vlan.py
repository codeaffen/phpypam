"""Tests to check funtionallity of vlan handling."""
import phpypam
import pytest
import vcr
import yaml

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS, FILTER_RESPONSE_HEADERS
from phpypam import PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

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


@vcr.use_cassette(cassette_name('test_create_vlan'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_create_vlan():
    """Test to create a new vlan.

    Create a vlan if it doesn't exists
    """
    try:
        entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    except PHPyPAMEntityNotFoundException:
        entity = pi.create_entity(controller='vlan', data=my_vlan)
        entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})

    assert entity is not None


@vcr.use_cassette(cassette_name('test_update_vlan'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_update_vlan():
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


@vcr.use_cassette(cassette_name('test_delete_vlan'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_delete_vlan():
    """Test to delete an existing vlan.

    Delete vlan which we created before
    """
    entity = pi.get_entity(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    pi.delete_entity(controller='vlan', controller_path=entity[0]['vlanId'])
    delete_kwargs = dict(controller='vlan', params={'filter_by': 'name', 'filter_value': my_vlan['name']})
    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **delete_kwargs)
