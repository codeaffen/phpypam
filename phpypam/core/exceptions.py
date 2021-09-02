"""Class to provided different Exceptions."""


class PHPyPAMException(Exception):
    """PHPyPAMExeption, children of :class:`Exception`.

    This exception is raised if anythings in :class:`phpypam.api` doesn't work out.
    """

    _NOT_FOUND_MESSAGES = {
        'No subnets found',
        'Address not found',
        'Vlan not found',
        'No vrfs configured',
        'No devices configured',
        'No results (filter applied)',
        'No objects found',
        'Hostname not found'
    }

    def __init__(self, *args, code=None, message=None):
        """Generate PHPyPAMException.

        This Exception takes 'code' and 'message' and decided on it which special Exception can be raised.

        :param code: Status code which comes from caller., defaults to None
        :type code: int, optional
        :param message: Optional message which comes from caller., defaults to None
        :type message: str, optional

        :raises PHPyPAMEntityNotFoundException: Exception if an entity was not found.
        :raises PHPyPAMInvalidCredentials: Exception if there are any issues with authentication.
        :raises PHPyPAMInvalidSyntax: Exception which is fired if there are syntax issues in talking to api.
        """
        self._code = code
        self._message = message

        if (self._code == 200 and self._message in self._NOT_FOUND_MESSAGES) or self._code == 404:
            raise PHPyPAMEntityNotFoundException(self._message)
        elif self._code == 500:
            if self._message == 'Invalid username or password':
                raise PHPyPAMInvalidCredentials(self._message)
        elif self._code == 400 or self._code == 503:
            raise PHPyPAMInvalidSyntax(message=self._message)

        # super(PHPyPAMException, self).__init__(*args, **kwargs)


class PHPyPAMInvalidCredentials(Exception):
    """Exception PHPyPAMInvalidCredentials, children of :class:`Exception`.

    This Exception is raised if there are any issues with the authentication against phpIPAM api.
    """

    def __init__(self, *args, **kwargs):
        """Generate PHPyPAMInvalidCredentials exception."""
        super(PHPyPAMInvalidCredentials, self).__init__(*args, **kwargs)


class PHPyPAMEntityNotFoundException(Exception):
    """Exception PHPyPAMEntityNotFoundException, children of :class:`Exception`.

    This Exception is raised if an entity was not found.
    """

    def __init__(self, *args, **kwargs):
        """Generate PHPyPAMEntityNotFoundException."""
        super(PHPyPAMEntityNotFoundException, self).__init__(*args, **kwargs)


class PHPyPAMInvalidSyntax(Exception):
    """Exception PHPyPAMInvalidSyntax, children of :class:`Exception`.

    This Exception is raised if there are any issues with syntax of request against phpIPAM api.
    """

    def __init__(self, *args, **kwargs):
        """Generate PHPyPAMInvalidSyntax exception."""
        self._message = kwargs.pop('message', '')

        super(PHPyPAMInvalidSyntax, self).__init__(self._message, *args, **kwargs)
