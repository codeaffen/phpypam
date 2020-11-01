"""Test controller method."""
import pytest
import phpypam
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


def test_controllers():
    """Test if controllers method returns correct datatype."""
    pi = phpypam.api(
        url=server['url'],
        app_id=server['app_id'],
        username=server['username'],
        password=server['password'],
        ssl_verify=True
    )

    controllers = pi.controllers()
    assert isinstance(controllers, set)
