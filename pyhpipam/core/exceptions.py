# provides the main query methods.

import json


class PyHPIPAMException(Exception):

    def __init__(self, *args, **kwargs):
        self._code = kwargs.pop('code', None)
        self._message = kwargs.pop('message', None)

        if self._code == 500:
            if self._message == 'Invalid username or password':
                raise PyHPIPAMInvalidCredentials(self._message)
        elif self._code == 400:
            raise PyHPIPAMInvalidSyntax(message=self._message)
        elif self._code == 404:
            raise PyHPIPAMEntityNotFoundException(self._message)

        # super(PyHPIPAMException, self).__init__(*args, **kwargs)


class PyHPIPAMInvalidCredentials(Exception):
    def __init__(self, *args, **kwargs):
        super(PyHPIPAMInvalidCredentials, self).__init__(*args, **kwargs)


class PyHPIPAMEntityNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(PyHPIPAMEntityNotFoundException, self).__init__(*args, **kwargs)


class PyHPIPAMInvalidSyntax(Exception):
    def __init__(self, *args, **kwargs):
        self._message = kwargs.pop('message', '')

        super(PyHPIPAMInvalidSyntax, self).__init__(self._message, *args, **kwargs)
