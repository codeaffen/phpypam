"""Test search for subnet."""
import pytest
import phpypam
import vcr
import yaml

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS, FILTER_RESPONSE_HEADERS
from phpypam import PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


@vcr.use_cassette(cassette_name('test_subnet_not_found'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_subnet_not_found(pi):
    """Test subnet not found exeption."""
    cidr = '10.0.0.0/24'
    search_kwargs = dict(controller='subnets', controller_path='cidr/' + cidr)

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)
