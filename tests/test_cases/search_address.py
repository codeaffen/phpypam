"""Test search for address."""
import pytest
import yaml

from phpypam import PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


def test_address_not_found(pi):
    """Test address not found execption."""
    addr = '10.10.0.4'
    search_kwargs = dict(controller='addresses', controller_path='search/' + addr)

    pytest.raises(PHPyPAMEntityNotFoundException, pi.get_entity, **search_kwargs)
