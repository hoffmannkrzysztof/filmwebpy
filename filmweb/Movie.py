# coding=utf-8
import sys

from filmweb.addon import BaseObject
from filmweb.parser.MovieParser import MovieParser
from filmweb.vars import filmweb_movie_link


class Movie(BaseObject):
    def __unicode__(self):
        """Return unicode title of Movie"""
        return u"%s" % self.title

    def __repr__(self):
        """Return string representation of an object"""
        return u"<movieID:%d title:_%s_>" % (self.objID, self.title.encode(sys.getdefaultencoding(), 'ignore'))

    __str__ = __repr__

    def __contains__(self, item):
        """Return true if this Person has worked in the given Movie"""
        from filmweb.Person import Person

        if isinstance(item, Person):
            for cast in self['cast']:
                if cast.isSame(item): return True

        return False

    def _parser(self):
        return MovieParser(self)

    def _get_url(self):
        from filmweb.parser import HTMLGrabber

        grabber = HTMLGrabber()
        f = grabber.open(filmweb_movie_link % ('film', 2000, self.objID))
        return f.url


