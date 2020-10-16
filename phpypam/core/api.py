# -*- coding: utf-8 -*-
# (c) Christian Meißner 2020

import json
import requests

from requests.auth import HTTPBasicAuth
from phpypam.core.exceptions import PHPyPAMException

GET = requests.get
POST = requests.post
PATCH = requests.patch
DELETE = requests.delete
OPTIONS = requests.options


class Api(object):

    def __init__(
        self,
        url,
        app_id,
        username=None,
        password=None,
        token=None,
        encryption=False,
        timeout=None,
        ssl_verify=True,
        user_agent=None
    ):
        self._api_url = url
        self._api_appid = app_id
        self._api_username = username
        self._api_password = password
        self._api_token = token
        self._api_encryption = encryption
        self._api_timeout = timeout
        self._api_ssl_verify = ssl_verify

        self._api_headers = {
            'content-type': 'application/json',
        }

        if user_agent:
            self._api_headers['user-agent'] = user_agent

        if not self._api_encryption:
            self._login()

    def _query(self, **kwargs):
        """ sends queries to phpIPAM API in a generalistic manner

        :param path: Path to the controler and possibly to function to use. Default is ```user```.
        :param method: method to be used for the query (choice: ```GET```, ```POST```, ```PATCH```, ```OPTIONS```).
        :param headers: Headers for request.
        :param data: (optional) Dictionary Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
        :param params: (optional) Dictionary list of tuples or bytes to send in the query string for the :class:`Request`.
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param token: (optional) Api token get from last login.
        """

        _api_path = kwargs.pop('path', 'user')
        _api_headers = kwargs.pop('headers', {})
        _method = kwargs.pop('method', 'GET')
        _data = kwargs.pop('data', None)
        _params = kwargs.pop('params', {})
        _auth = kwargs.pop('auth', None)

        if self._api_token:
            _api_headers['token'] = self._api_token

        _url = '{}/api/{}/{}'.format(self._api_url, self._api_appid, _api_path)

        if _params and not _url.endswith('/'):
            _url = _url + '/'

        resp = _method(
            _url,
            params=_params,
            data=_data,
            headers=_api_headers,
            auth=_auth,
            verify=self._api_ssl_verify,
            timeout=self._api_timeout,
        )

        result = resp.json()

        if result['code'] not in (200, 201) or not result['success']:
            raise PHPyPAMException(code=result['code'], message=result['message'])
        else:
            if 'data' in result:
                return result['data']

    def _login(self):
        _auth = HTTPBasicAuth(self._api_username, self._api_password)
        resp = self._query(method=POST, auth=_auth)

        self._api_token = resp['token']

    def get_token(self):
        return self._api_token

    def get_entity(self, controller, **kwargs):
        _path = controller
        _controller_path = kwargs.pop('controller_path', None)
        _params = kwargs.pop('params', None)

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=GET, path=_path, params=_params)

    def create_entity(self, controller, data, **kwargs):
        _path = controller
        _controller_path = kwargs.pop('controller_path', None)
        _params = kwargs.pop('params', None)

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=POST, path=_path, data=data, params=_params)

    def delete_entity(self, controller, controller_path, **kwargs):
        _path = '{}/{}'.format(controller, controller_path)
        _params = kwargs.pop('params', None)

        return self._query(token=self._api_token, method=DELETE, path=_path, params=_params)

    def update_entity(self, controller, data, **kwargs):
        _path = controller
        _controller_path = kwargs.pop('controller_path', None)
        _params = kwargs.pop('params', None)

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=PATCH, path=_path, data=data, params=_params)

    def controllers(self):
        result = self._query(token=self._api_token, method=OPTIONS, path='/')

        controllers = ({v for ctrl in result['controllers'] for (k, v) in ctrl.items() if k == 'rel'})

        return controllers
