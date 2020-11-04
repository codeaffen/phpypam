"""Tests to check section search via url parameters."""
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


@vcr.use_cassette(cassette_name('test_search_not_existing_section'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_search_not_existing_section():
    """Search for non existing section.

    Search for a non existign section and get NotFound exception
    """
    search_term = {'filter_by': 'name', 'filter_value': 'non_existing_section'}
    search_kwargs = dict(controller='sections', params=search_term)
    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)


@vcr.use_cassette(cassette_name('test_search_existing_section'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_search_existing_section():
    """Search for existing section.

    Search for an existing section
    """
    search_term = {'filter_by': 'name', 'filter_value': 'IPv6', 'filter_match': 'full'}
    entity = pi.get_entity(controller='sections', params=search_term)

    assert entity is not None
