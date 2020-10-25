# provides the main query methods.

import json


class PHPyPAMException(Exception):

    def __init__(self, *args, **kwargs):
        self._code = kwargs.pop('code', None)
        self._message = kwargs.pop('message', None)

        _NOT_FOUND_MESSAGES = {
            'No subnets found',
            'Address not found',
        }

        if (self._code == 200 and self._message in _NOT_FOUND_MESSAGES) or self.code == 404:
            raise PHPyPAMEntityNotFoundException(self._message)
        elif self._code == 500:
            if self._message == 'Invalid username or password':
                raise PHPyPAMInvalidCredentials(self._message)
        elif self._code == 400:
            raise PHPyPAMInvalidSyntax(message=self._message)

        # super(PHPyPAMException, self).__init__(*args, **kwargs)


class PHPyPAMInvalidCredentials(Exception):
    def __init__(self, *args, **kwargs):
        super(PHPyPAMInvalidCredentials, self).__init__(*args, **kwargs)


class PHPyPAMEntityNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(PHPyPAMEntityNotFoundException, self).__init__(*args, **kwargs)


class PHPyPAMInvalidSyntax(Exception):
    def __init__(self, *args, **kwargs):
        self._message = kwargs.pop('message', '')

        super(PHPyPAMInvalidSyntax, self).__init__(self._message, *args, **kwargs)
