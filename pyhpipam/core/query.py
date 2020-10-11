# provides the main query methods.

import json


class InvalidUsernameOrPasswordException(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidUsernameOrPasswordException, self).__init__(*args, **kwargs)


class EntityNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(EntityNotFoundException, self).__init__(*args, **kwargs)


class ParameterNotDefinedException(Exception):
    def __init__(self, *args, **kwargs):
        super(ParameterNotDefinedException, self).__init__(*args, **kwargs)


def query(**kwargs):
    """ sends queries to phpIPAM API in a generalistic manner

    :param url: URL to the api of the phpIPAM instace. Needs to include the used scheme like ```https://``` or ```http://```.
    :param path: Path to the controler and possibly to function to use. Default is ```user```.
    :param app_id: Name of the app id used for this request.
    :param method: method to be used for the query (choice: ```GET```, ```POST```, ```PATCH```, ```OPTIONS```).
    :param headers: Headers for request.
    :param timeout: Timeout for request.
    :param verify: Should ssl certificate be verified. Default ```False```.
    :param data: (optional) Dictionary Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    :param params: (optional) Dictionary list of tuples or bytes to send in the query string for the :class:`Request`.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param token: (optional) Api token get from last login.
    """

    _api_url = kwargs.pop('url', None)
    _api_path = kwargs.pop('path', 'user')
    _api_appid = kwargs.pop('app_id', None)
    _api_headers = kwargs.pop('headers', {})
    _method = kwargs.pop('method', 'GET')
    _data = kwargs.pop('data', None)
    _params = kwargs.pop('params', {})
    _auth = kwargs.pop('auth', None)
    _api_token = kwargs.pop('token', None)
    _api_timeout = kwargs.pop('timeout', None)
    _api_ssl_verify = kwargs.pop('verify', False)

    if _api_url is None:
        raise ParameterNotDefinedException('Parameter `url` not defined.')

    if _api_appid is None:
        raise ParameterNotDefinedException('Parameter `app_id` not defined.')

    if _api_token:
        _api_headers['token'] = _api_token

    _url = '{}/api/{}/{}'.format(_api_url, _api_appid, _api_path)

    if _data is not None:
        _data = json.dumps(_data)

    resp = _method(
        _url,
        params=_params,
        data=_data,
        headers=_api_headers,
        auth=_auth,
        verify=_api_ssl_verify,
        timeout=_api_timeout,
    )

    result = resp.json()

    if result['code'] not in (200, 201) or not result['success']:
        if result['code'] == 500:
            if result['message'] == 'Invalid username or password':
                raise InvalidUsernameOrPasswordException(result['message'])
        elif result['code'] == 404:
            if result['message'] == 'Not Found':
                raise EntityNotFoundException(result['message'])
    else:
        if 'data' in result:
            return result['data']
