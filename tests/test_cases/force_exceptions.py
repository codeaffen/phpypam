"""Test exceptions."""
import phpypam
import pytest
import yaml

from phpypam.core.exceptions import PHPyPAMEntityNotFoundException, PHPyPAMInvalidCredentials, PHPyPAMInvalidSyntax


with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


def test_invalid_syntax_exception():
    """Test invalid syntax exception.

    Test if PHPyPAMInvalidSyntax exception is fired corretly.
    """
    connection_kwargs = server.copy()
    connection_kwargs.update({'app_id': 'faulty data'})

    with pytest.raises(PHPyPAMInvalidSyntax, match='Invalid application id'):
        phpypam.api(**connection_kwargs)


def test_invalid_credentials_exception():
    """Test invalid credentials exception.

    Test if ...
    """
    connection_kwargs = server.copy()
    connection_kwargs.update({'username': 'faulty data'})
    with pytest.raises(PHPyPAMInvalidCredentials):
        phpypam.api(**connection_kwargs)

    connection_kwargs.update({'username': server['username'], 'password': 'wrong_data'})
    with pytest.raises(PHPyPAMInvalidCredentials):
        phpypam.api(**connection_kwargs)


def test_entity_not_found_execption(pi):
    """Test not found execption on empty subnet.

    Create an empty subnet, search for addresses and get not found exception.
    """
    my_subnet = dict(
        subnet='172.16.0.0',
        mask=24,
        description='Test subnet',
        sectionId=1,
    )

    try:
        entity = pi.get_entity(controller='subnets',
                               controller_path="cidr/{}/{}".format(my_subnet['subnet'], my_subnet['mask']),
                               params={'filter_by': 'sectionId', 'filter_value': my_subnet['sectionId']})
    except PHPyPAMEntityNotFoundException:
        entity = pi.create_entity(controller='subnets', data=my_subnet)
        entity = pi.get_entity(controller='subnets', controller_path="cidr/{}/{}".format(my_subnet['subnet'], my_subnet['mask']))

    if len(entity) > 0 and len(entity) < 2:
        entity = entity[0]
    else:
        pytest.fail('Wrong number of entities found')

    print(entity)
    with pytest.raises(PHPyPAMEntityNotFoundException):
        pi.get_entity(controller='subnets', controller_path=entity['id'] + '/addresses')

    pi.delete_entity(controller='subnets', controller_path=entity['id'])
