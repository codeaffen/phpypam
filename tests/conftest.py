"""Provide some base configurations for tests."""
import phpypam
import pytest
import py.path
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
    ssl_verify = kwargs.pop('ssl_verify', True)

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


def pytest_addoption(parser):
    """Change command line options defaults.

    We want run our tests only in three modes
    `live` - interact with an existing API
    `record` - interact with an existing API and record the interactions
    `replay` - replay previouly recorded interactions with API

    :param parser: A parser object
    :type parser: object parser
    """
    parser.addoption(
        "--vcrmode",
        action="store",
        default="replay",
        choices=["replay", "record", "live"],
        help="mode for vcr recording; one of ['replay', 'record', 'live']",
    )


@pytest.fixture
def vcrmode(request):
    """Return vcrmode of a request.

    :param request: A request object
    :type request: object request
    :return: vcrmode
    :rtype: str
    """
    return request.config.getoption("vcrmode")


def cassette_name(test_name=None):
    """Generate cassette_name."""
    return 'tests/fixtures/{0}.yml'.format(test_name)


FILTER_REQUEST_HEADERS = ['Authorization', 'Cookie', 'Token']
FILTER_RESPONSE_HEADERS = ['Apipie-Checksum', 'Date', 'ETag', 'Server', 'Set-Cookie', 'Via', 'X-Powered-By', 'X-Request-Id', 'X-Runtime']


def filter_response(response):
    """Filter headers before recording.

    :param response: A response object where we want to filter the headers from.
    :type response: object response
    :return: response
    :rtype: object response
    """
    for header in FILTER_RESPONSE_HEADERS:
        # headers should be case insensitive, but for some reason they weren't for me
        response['headers'].pop(header.lower(), None)
        response['headers'].pop(header, None)

    return response


def filter_request_uri(request):
    """Filter uri before recording.

    :param request: A request object where we want to filter the uri from.
    :type request: object request
    :return: request
    :rtype: object request
    """
    request.uri = urlunparse(urlparse(request.uri)._replace(netloc="ipam.example.org"))
    return request
