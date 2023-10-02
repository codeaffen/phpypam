"""Test exceptions."""
import phpypam
import pytest
import yaml

from phpypam.core.exceptions import PHPyPAMException, PHPyPAMEntityNotFoundException


with open('tests/vars/server.yml') as conn:
    connection_params = yaml.safe_load(conn)

with open('tests/vars/search_exceptions.yml') as config:
    not_found_cases = yaml.safe_load(config)['not_found_cases']


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
