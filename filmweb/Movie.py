# coding=utf-8
from filmweb.addon import BaseObject
import sys

class Movie(BaseObject):

    def __unicode__(self):
        """Return unicode title of Movie"""
        return u"%s" % self.title

    def __repr__(self):
        """Return string representation of an object"""
        return u"<movieID:%d title:_%s_>" % (self.objID,self.title.encode(sys.getdefaultencoding(),'ignore'))
    __str__ = __repr__

