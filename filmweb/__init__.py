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
    movie =  movies[0]
    person =fa.get_person(4146)
    print person in movie

    #for cast in movies[0]['cast']:
    #    print cast.title,cast.roleType,cast.roleName



if __name__ == "__main__":
    main()
