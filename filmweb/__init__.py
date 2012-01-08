# coding=utf-8
from filmweb._exceptions import FilmwebParserError
from filmweb.parser import FilmwebHTTP

def Filmweb(access=None, *arguments, **keywords):

    if access == 'http':
        return FilmwebHTTP()
    else:
        raise FilmwebParserError('Unknown data system: %s' % access)


def main():
    fa = Filmweb('http')
    print fa.search_movie('Mad')

if __name__ == "__main__":
    main()
