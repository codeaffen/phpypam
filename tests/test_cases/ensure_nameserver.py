"""Tests to check funtionallity of section handling."""
import phpypam
import pytest
import vcr
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS, FILTER_RESPONSE_HEADERS
from phpypam import PHPyPAMEntityNotFoundException


my_nameserver = dict(
    name='my dns',
    namesrv1='127.0.01',
    permissions=1,
)


@vcr.use_cassette(cassette_name('test_create_nameserver'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_create_nameserver(pi):
    """Test to create a new nameserver.

    Create a nameserver if it doesn't exists
    """
    try:
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    except PHPyPAMEntityNotFoundException:
        entity = pi.create_entity(controller='tools/nameservers', data=my_nameserver)
        entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    assert entity is not None


@vcr.use_cassette(cassette_name('test_update_nameserver'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_update_nameserver(pi):
    """Test to update an existing nameserver.

    Update one field of an existing nameserver
    """
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    my_nameserver.update({'description': 'description added'})

    pi.update_entity(controller='tools/nameservers', controller_path=entity[0]['id'], data=my_nameserver)
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    assert entity[0]['description'] == my_nameserver['description']


@vcr.use_cassette(cassette_name('test_delete_nameserver'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_delete_nameserver(pi):
    """Test to delete an existing nameserver.

    Delete the nameserver which we created before
    """
    entity = pi.get_entity(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})
    pi.delete_entity(controller='tools/nameservers', controller_path=entity[0]['id'])
    delete_kwargs = dict(controller='tools/nameservers', params={'filter_by': 'name', 'filter_value': my_nameserver['name']})

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **delete_kwargs)
