# coding=utf-8
from filmweb.parser import ParserBase


class FilmwebHTTP(ParserBase):

    def _search_movie(self,title,results=None):
        #http://www.filmweb.pl/search/film?q=piraci&page=1
        """Return list of movies"""

    def _search_person(self,name,results=None):
        #http://www.filmweb.pl/search/person?q=Tom+Cruise
        """Return list of persons"""

    def _get_person(self,personID):
        """Return Person object"""

    def _get_movie(self,movieID):
        """Return Movie object"""