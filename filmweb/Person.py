# coding=utf-8
from filmweb.addon import BaseObject
import sys
from filmweb.parser.PersonParser import PersonParser
from vars import filmweb_person_link

class Person(BaseObject):

    def __unicode__(self):
        """Return unicode title of Person"""
        return u"%s" % self.title

    def __repr__(self):
        """Return string representation of an object"""
        return u"<personID:%d title:_%s_>" % (self.objID,self.title.encode(sys.getdefaultencoding(),'ignore'))
    __str__ = __repr__

    def _parser(self):
        return PersonParser(self)

    def _get_url(self):
        from filmweb.parser import HTMLGrabber
        grabber = HTMLGrabber()
        f = grabber.open( filmweb_person_link % ('name',self.objID) )
        return f.url



