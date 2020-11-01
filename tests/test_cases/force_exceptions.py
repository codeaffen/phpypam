"""Test exceptions."""
import pytest
import phpypam
import json
import yaml

from phpypam.core.exceptions import PHPyPAMException, PHPyPAMEntityNotFoundException, PHPyPAMInvalidCredentials, PHPyPAMInvalidSyntax

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


connection_params = dict(
    url=server['url'],
    app_id=server['app_id'],
    username=server['username'],
    password=server['password'],
    ssl_verify=True
)


def test_invalid_syntax_exception():
    """Test invalid syntax exception.

    Test if PHPyPAMInvalidSyntax exception is fired corretly.
    """
    connection_params.update({'app_id': 'faulty data'})

    with pytest.raises(PHPyPAMInvalidSyntax, match='Invalid application id'):
        phpypam.api(**connection_params)

    connection_params.update({'app_id': server['app_id']})


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
