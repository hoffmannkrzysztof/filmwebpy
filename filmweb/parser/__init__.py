# coding=utf-8


class ParserBase(object):

    def __repr__(self):
        """Return string representation of parser object"""
        return u'<Filmweb: %s>' % (self.__class__.__name__)

    def _search_movie(self, title, results):
        raise NotImplementedError()

    def _search_person(self, name, results):
        raise NotImplementedError()

    def _get_person(self,personID):
        raise NotImplementedError()

    def _get_movie(self,movieID):
        raise NotImplementedError()

    def search_movie(self, title, results=20):
        """Return a list of Movie objects for a query for the given title."""
        try:
            results = int(results)
        except ValueError:
            results = 20

        res = self._search_movie(title, results)
        return []

    def search_person(self, name, results=20):
        """Return a list of Person objects for a query for the given name.."""
        try:
            results = int(results)
        except ValueError:
            results = 20

        res = self._search_person(name, results)
        return [] #list of Person objects

    def get_movie(self, movieID):
        """Return a Movie object of given MovieID"""
        return movie

    def get_person(self, personID):
        """Return a Person object for the given personID."""
        return person

