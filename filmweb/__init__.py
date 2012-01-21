# coding=utf-8
from filmweb._exceptions import FilmwebParserError
from filmweb.parser import FilmwebHTTP

def Filmweb(access=None):

    if access == 'http':
        return FilmwebHTTP()
    else:
        raise FilmwebParserError('Unknown data system: %s' % access)


def main():
    fa = Filmweb('http')
    movies = fa.search_movie('piraci')
    print movies
    print movies[0]['cast']

if __name__ == "__main__":
    main()
