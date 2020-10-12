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
            if self._message == 'Not Found':
                raise EntityNotFoundException(self._message)

        # super(PyHPIPAMException, self).__init__(*args, **kwargs)


class PyHPIPAMInvalidCredentials(Exception):
    def __init__(self, *args, **kwargs):
        super(PyHPIPAMInvalidCredentials, self).__init__(*args, **kwargs)


class EntityNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(EntityNotFoundException, self).__init__(*args, **kwargs)


class PyHPIPAMInvalidSyntax(Exception):
    def __init__(self, *args, **kwargs):
        self._message = kwargs.pop('message', '')

        super(PyHPIPAMInvalidSyntax, self).__init__(self._message, *args, **kwargs)
