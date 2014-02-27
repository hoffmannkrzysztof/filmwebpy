# coding=utf-8
from filmweb._exceptions import FilmwebParserError
from filmweb.parser import FilmwebHTTP


def Filmweb(access='http'):
    if access == 'http':
        return FilmwebHTTP()
    else:
        raise FilmwebParserError('Unknown data system: %s' % access)
