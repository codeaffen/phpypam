"""Test exceptions."""
import phpypam
import pytest
import vcr
import yaml

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS
from phpypam.core.exceptions import PHPyPAMException, PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as conn:
    connection_params = yaml.safe_load(conn)

with open('tests/vars/search_exceptions.yml') as config:
    not_found_cases = yaml.safe_load(config)['not_found_cases']


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
        assert str(e.value) in PHPyPAMException._NOT_FOUND_MESSAGES
