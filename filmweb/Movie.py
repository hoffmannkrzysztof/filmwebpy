# coding=utf-8
from filmweb.addon import BaseObject

class Movie(BaseObject):

    def __init__(self,MovieID,title=None,data={}):
        self.MovieID = MovieID
        self.set_data(data)
        self.set_title(title)


    def __str__(self):
        """Return string title of Movie"""
        return "%s" % self.title.encode('utf-8', 'replace')

    def __unicode__(self):
        """Return unicode title of Movie"""
        return u"%s" % self.title

    def __repr__(self):
        """Return string representation of an object"""
        return u'<Movie id:%s[%s] title:_%s_>' % (self.movieID,self.title)
