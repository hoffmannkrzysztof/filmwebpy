# coding=utf-8

import logging

class FilmwebError(Exception):
    """Base class for every exception raised by the filmweb package."""
    _logger = logging.getLogger('filmwebpy')

    def __init__(self, *args, **kwargs):
        self._logger.critical('%s exception raised; args: %s; kwds: %s',
            self.__class__.__name__, args, kwargs,
            exc_info=True)
        Exception.__init__(self, *args, **kwargs)

class FilmwebDataAccessError(FilmwebError):
    """Exception raised when is not possible to receive data."""
    pass

class FilmwebParserError(FilmwebError):
    """Exception raised when an error occurred parsing the data."""
    pass