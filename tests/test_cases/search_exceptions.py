"""Test exceptions."""
from vcr import record_mode
import phpypam
import pytest
import vcr
import yaml

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS
from phpypam.core.exceptions import PHPyPAMException, PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

connection_params = dict(
    url=server['url'],
    app_id=server['app_id'],
    username=server['username'],
    password=server['password'],
    ssl_verify=True
)

not_found_messages = PHPyPAMException._NOT_FOUND_MESSAGES

not_found_cases = [
    dict(controller='subnets', path='cidr/1.2.3.4', params=None),
    dict(controller='addresses', path='search/1.2.3.4'),
    dict(controller='vlans', path='/1337'),
    dict(controller='vrf'),
    dict(controller='devices', path='/1337'),
    dict(controller='sections', params={'filter_by': 'name', 'filter_value': 'not_existing_section', 'filter_match': 'full'}),
    dict(controller='tools/device_types', path='/1337'),
    dict(controller='addresses', path=f"search_hostname/not_existing_hostname/")
]


@vcr.use_cassette(cassette_name('test_entity_not_found_exception'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response,
                  record_mode='rewrite'
                  )
@pytest.mark.parametrize('case', not_found_cases)
def test_entity_not_found_exception(case):
    """Test entity not found exception.

    Test if PHPyPAMEntityNotFound exception is fired corretly for all cases.
    """

    pi = phpypam.api(**connection_params)

    # check whether PHPyPAMEntityNotFoundException is raised
    with pytest.raises(PHPyPAMEntityNotFoundException) as e:
        pi.get_entity(case['controller'], controller_path=case.pop('path', None), params=case.pop('params', None))

        # assert exception message is in all not found outputs
        assert e.value.args[0] in not_found_cases
