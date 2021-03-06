"""Test exceptions."""
import phpypam
import pytest
import vcr
import yaml

from tests.conftest import filter_request_uri, filter_response, cassette_name, FILTER_REQUEST_HEADERS
from phpypam.core.exceptions import PHPyPAMInvalidCredentials, PHPyPAMInvalidSyntax


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

connection_params = dict(
    url=server['url'],
    app_id=server['app_id'],
    username=server['username'],
    password=server['password'],
    ssl_verify=True
)


@vcr.use_cassette(cassette_name('test_invalid_syntax_exception'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_invalid_syntax_exception():
    """Test invalid syntax exception.

    Test if PHPyPAMInvalidSyntax exception is fired corretly.
    """
    connection_params.update({'app_id': 'faulty data'})

    with pytest.raises(PHPyPAMInvalidSyntax, match='Invalid application id'):
        phpypam.api(**connection_params)

    connection_params.update({'app_id': server['app_id']})


@vcr.use_cassette(cassette_name('test_invalid_credentials_exception'),
                  filter_headers=FILTER_REQUEST_HEADERS,
                  before_record_request=filter_request_uri,
                  before_recorde_response=filter_response
                  )
def test_invalid_credentials_exception():
    """Test invalid credentials exception.

    Test if ...
    """
    connection_params.update({'username': 'faulty data'})
    with pytest.raises(PHPyPAMInvalidCredentials):
        phpypam.api(**connection_params)

    connection_params.update({'username': server['username'], 'password': 'wrong_data'})
    with pytest.raises(PHPyPAMInvalidCredentials):
        phpypam.api(**connection_params)

    connection_params.update({'password': server['password']})
