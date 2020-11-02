"""Test search for address."""
import pytest
import phpypam
import json
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

from phpypam import PHPyPAMEntityNotFoundException


def test_address_not_found():
    """Test address not found execption."""
    pi = phpypam.api(
        url=server['url'],
        app_id=server['app_id'],
        username=server['username'],
        password=server['password'],
        ssl_verify=True
    )

    addr = '10.10.0.4'

    search_kwargs = dict(controller='addresses', controller_path='search/' + addr)

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)
