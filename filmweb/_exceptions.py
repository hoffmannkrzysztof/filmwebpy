# coding=utf-8


class FilmwebError(Exception):
    """Base class for every exception raised by the filmweb package."""


class FilmwebDataAccessError(FilmwebError):
    """Exception raised when is not possible to receive data."""
    pass


class FilmwebParserError(FilmwebError):
    """Exception raised when an error occurred parsing the data."""
    pass