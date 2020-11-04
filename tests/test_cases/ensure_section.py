"""Tests to check funtionallity of section handling."""
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

my_section = dict(
    name='foobar',
    description='new section',
    permissions='{"3":"1","2":"2"}'
)


@vcr.use_cassette(cassette_name('test_create_section'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
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


@vcr.use_cassette(cassette_name('test_update_section'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_update_section():
    """Test to update an existing section.

    Update one field of an existing section.
    """
    my_section['description'] = 'new description'

    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    pi.update_entity(controller='sections', controller_path=entity['id'], data=my_section)
    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])

    assert entity['description'] == my_section['description']


@vcr.use_cassette(cassette_name('test_delete_section'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_delete_section():
    """Test to delete an existing section.

    Delete one field of an existing section.
    """
    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
    pi.delete_entity(controller='sections', controller_path=entity['id'])
    entity_kwargs = dict(controller='sections', controller_path=my_section['name'])
    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **entity_kwargs)
