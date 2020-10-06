# -*- coding: utf-8 -*-
# (c) Christian Meißner 2020

# pylint: disable=raise-missing-from
# pylint: disable=super-with-arguments

import requests

from requests.auth import HTTPBasicAuth
from pyhpipam.core.query import query

GET = requests.get
POST = requests.post
PATCH = requests.patch
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

    def _login(self):
        _auth = HTTPBasicAuth(self._api_username, self._api_password)
        resp = query(url=self._api_url, app_id=self._api_appid, method=POST, auth=_auth, verify=self._api_ssl_verify)

        self._token = resp['token']

    def get_token(self):
        return self._token
