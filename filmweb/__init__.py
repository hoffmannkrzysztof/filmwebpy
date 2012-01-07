# coding=utf-8
from filmweb._exceptions import FilmwebParserError
from parser.http import FilmwebHTTP
def Filmweb(access=None, *arguments, **keywords):
    if access == 'http':
        return FilmwebHTTP()
    else:
        raise FilmwebParserError('Unknown data system: %s' % access)
