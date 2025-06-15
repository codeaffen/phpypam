"""Provide some base configurations for tests."""
import phpypam
import pytest
import py.path  # pyright: ignore reportMissingImports=false
import yaml

from urllib.parse import urlparse, urlunparse

TEST_CASES_PATH = py.path.local(__file__).realpath() / '..' / 'test_cases'

with open('tests/vars/server.yml') as c:
    server = yaml.safe_load(c)


@pytest.fixture(scope='module')
def pi(*arg, **kwargs):
    """Create a phpypam.api object and return it.

    :return: object phpypam
    :rtype: phpypam.api
    """
    url = kwargs.pop('url', server['url'])
    app_id = kwargs.pop('app_id', server['app_id'])
    username = kwargs.pop('username', server['username'])
    password = kwargs.pop('password', server['password'])
    ssl_verify = kwargs.pop('ssl_verify', server['ssl_verify'])

    return phpypam.api(
        url=url,
        app_id=app_id,
        username=username,
        password=password,
        ssl_verify=ssl_verify,
        **kwargs
    )


def find_all_test_cases():
    """Generate list of test cases.

    :yield: generates each test case as list item
    :rtype: str
    """
    for c in TEST_CASES_PATH.listdir(sort=True):
        c = c.basename
        if c.endswith('.py'):
            yield c.replace('.py', '')


TEST_CASES = list(find_all_test_cases())
