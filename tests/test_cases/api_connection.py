"""Tests to check connection to API."""
import phpypam
import pytest
import yaml

from phpypam.core.exceptions import PHPyPAMInvalidCredentials

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

connection_params = dict(
    url=server['url'],
    app_id=server['app_id'],
    username=server['username'],
    password=server['password'],
    ssl_verify=True
)


def test_connection_success():
    """Test whether a connection to API can be done."""
    pi = phpypam.api(**connection_params)

    token = pi.get_token()

    assert isinstance(pi, phpypam.api)
    assert len(token) == 24


def test_connection_failure():
    """Test faulty connection.

    Test if failure where reported correctly if there is faulty login data.
    """
    connection_kwargs = connection_params.copy()
    connection_kwargs.update({'password': 'wrong_password'})

    pytest.raises(PHPyPAMInvalidCredentials, phpypam.api, **connection_kwargs)

    connection_kwargs = connection_params.copy()
    connection_kwargs.update({'username': 'wrong_username'})

    pytest.raises(PHPyPAMInvalidCredentials, phpypam.api, **connection_kwargs)


def test_custom_user_agent():
    """Test to set custom user-agent header.

    Test to connect to API with a custom user-agent header set.
    """
    connection_kwargs = connection_params.copy()
    connection_kwargs.update({'user_agent': 'my_test_agent'})

    pi = phpypam.api(**connection_kwargs)

    assert isinstance(pi, phpypam.api)
    assert len(pi.get_token()) == 24
