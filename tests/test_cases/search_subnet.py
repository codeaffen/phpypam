"""Test search for subnet."""
import pytest
import phpypam
import json
import yaml

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)

from phpypam import PHPyPAMEntityNotFoundException


def test_subnet_not_found():
    """Test subnet not found exeption."""
    pi = phpypam.api(
        url=server['url'],
        app_id=server['app_id'],
        username=server['username'],
        password=server['password'],
        ssl_verify=True
    )

    cidr = '10.0.0.0/24'

    search_kwargs = dict(controller='subnets', controller_path='cidr/' + cidr)

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)
