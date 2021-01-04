# -*- coding: utf-8 -*-
# (c) Christian Meißner 2020
"""Default class to handle all api interactions with phpIPAM server."""
import re
import requests

from requests.auth import HTTPBasicAuth
from phpypam.core.exceptions import PHPyPAMException

GET = requests.get
POST = requests.post
PATCH = requests.patch
DELETE = requests.delete
OPTIONS = requests.options


class Api(object):
    """The main class.

    It generates tha API object where you can run
    different actions again to `create`, `update` and `delete` entities.
    It also provides functions with informational character only.
    """

    def __init__(self, url, app_id, username=None, password=None, token=None, encryption=False, timeout=None, ssl_verify=True, user_agent=None):
        """Generate the api object.

        The costructor collects all data to connect to phpIPAM API. If all data is there it makes the connection to the given server.

        :param url: The URL to a phpIPAM instance. It includes the protocol (`https` or `http`).
            As phpIPAM does not support `http` and `User token` by default you have to configure phpIPAM to allow unsecure connections.
            But be aware on security risk in conjunction with this setting.
        :type url: str
        :param app_id: The app_id which is used for the API operations.
            For modifying operations it needs read/write access.
        :type app_id: str
        :param username: The `username` which is used to connect to API., defaults to None
        :type username: str, optional
        :param password: The `password` to authenticate `username` against API., defaults to None
        :type password: str, optional
        :param token: A `token` if you want to use token based authentication., defaults to None
        :type token: str, optional
        :param encryption: Should request be encrypted. This is the needed encryption string., defaults to False
        :type encryption: bool, optional
        :param timeout: Seconds until a request will time out., defaults to None
        :type timeout: int, optional
        :param ssl_verify: Should certificate of endpoint verified or not.
            Useful if you use a self signed certificate., defaults to True
        :type ssl_verify: bool, optional
        :param user_agent: With this parameter you can define a own user agent header string., defaults to None
        :type user_agent: str, optional
        """
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

    def _query(self, path='user', headers=None, method=GET, data=None, params=None, auth=None, token=None):
        """Send queries to phpIPAM API in a generalistic manner.

        :param path: Path to the controler and possibly to function to use., defaults to 'user'
        :type path: str, optional
        :param headers: Optional request headers, defaults to None
        :type headers: dict, optional
        :param method: method to be used for the query (choice: 'GET', 'POST', 'PATCH', 'OPTIONS')., defaults to GET
        :type method: requests method object, optional
        :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:'Request'., defaults to None
        :type data: dict, optional
        :param params: Dictionary list of tuples or bytes to send in the query string for the :class:'Request'., defaults to None
        :type params: dict, optional
        :param auth: Auth tuple to enable Basic/Digest/Custom HTTP Auth., defaults to None
        :type auth: HTTPBasicAuth object, optional
        :type auth: str, optional
        :param token: Api token get from last login., defaults to None
        :type token: str, optional

        :raises PHPyPAMException: [description]

        :return: If query returns any data it returns this dict or list else it returns last exit status
        :rtype: Union[bool, dict, list]
        """
        _api_path = path
        _api_headers = headers or {}
        _method = method
        _data = data
        _params = params
        _auth = auth

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
        """Login to phpIPAM API and return token."""
        _auth = HTTPBasicAuth(self._api_username, self._api_password)
        resp = self._query(method=POST, auth=_auth)

        self._api_token = resp['token']

    def get_token(self):
        """Return last login token.

        :return: Returns the api token from the last successful login.
        :rtype: str
        """
        return self._api_token

    def get_entity(self, controller, controller_path=None, params=None):
        """Get existing entity from phpIPAM server.

        This method query for existing entity. It there a result it will be returned otherwise
        an PhpIPAMEntityNotFound exception is raised from underlying method.

        :param controller: Name of the controller to request entity from.
        :type controller: str
        :param controller_path: The path which is used to query for entities, defaults to None
        :type controller_path: str, optional
        :param params: Request parameters which have to be append to the request URI, defaults to None
        :type params: dict, optional

        :return: Result of the query. It can be either a 'list' or 'dict'.
        :rtype: Union[dict, list]
        """
        _path = controller
        _controller_path = controller_path
        _params = params

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=GET, path=_path, params=_params)

    def create_entity(self, controller, controller_path=None, data=None, params=None):
        """Create an entity.

        :param controller: Name of the controller to use.
        :type controller: str
        :param controller_path: The path which is used to query for entities, defaults to None
        :type controller_path: str, optional
        :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
        :type data: dict
        :param params: Dictionary list of tuples or bytes to send in the query string for the :class:`Request`., defaults to None
        :type params: dict, optional

        :return: Returns the newly created entity.
        :rtype: Union[dict, list]
        """
        _path = controller
        _controller_path = controller_path
        _params = params

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=POST, path=_path, data=data, params=_params)

    def delete_entity(self, controller, controller_path, params=None):
        """Delete an entity.

        :param controller: Name of the controller to use.
        :type controller: str
        :param controller_path: The path wich is used to access the entity to delete.
        :type controller_path: str
        :param params: Dictionary, list of tuples or bytes to send in the query string for the :class:`Request`., defaults to None
        :type params: dict, optional

        :return: Returns True if entity was deleted successfully or either 'dict' or 'list' of entities to work on.
        :rtype: Union[book, dict, list]
        """
        _path = '{}/{}'.format(controller, controller_path)
        _params = params

        return self._query(token=self._api_token, method=DELETE, path=_path, params=_params)

    def update_entity(self, controller, controller_path=None, data=None, params=None):
        """Update an entity.

        :param controller: Name of the controller to use.
        :type controller: str
        :param controller_path: The path which is used to access the entity to update., defaults to None
        :type controller_path: str, optional
        :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`., defaults to None
        :type data: dict, optional
        :param params: Dictionary list of tuples or bytes to send in the query string for the :class:`Request`., defaults to None
        :type params: dict, optional

        :return: Returns either a 'dict' or 'list' of the changed entity
        :rtype: Union[dict, list]
        """
        _path = controller
        _controller_path = controller_path
        _params = params

        if _controller_path:
            _path = '{}/{}'.format(_path, _controller_path)

        return self._query(token=self._api_token, method=PATCH, path=_path, data=data, params=_params)

    def controllers(self):
        """Report all controllers from phpIPAM API.

        This method is used to report all known controllers of phpIPAM API.
        Unfortunately the API doesn't report all nor the correct paths for all 'controllers'.

        :return: Returns a tuple of controller paths.
        :rtype: tuple
        """
        result = self._query(token=self._api_token, method=OPTIONS, path='/')

        controllers = ({re.sub(r'^/api/' + self._api_appid + '/(.+)/$', r'\1', v) for ctrl in result['controllers'] for (k, v) in ctrl.items() if k == 'href'})

        return controllers
