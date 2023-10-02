"""Test search for subnet."""
import pytest
import yaml

from phpypam import PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


def test_subnet_not_found(pi):
    """Test subnet not found exeption."""
    cidr = '10.0.0.0/24'
    search_kwargs = dict(controller='subnets', controller_path='cidr/' + cidr)

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)
