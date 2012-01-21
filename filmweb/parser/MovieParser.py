# coding=utf-8
from urlparse import urljoin
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
from filmweb.parser import HTMLGrabber
from filmweb.vars import filmweb_root

class MovieParser(object):

    def __init__(self,movie):
        self.movie = movie

    def parse_cast(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.movie.url+"/cast" )
        soup = BeautifulSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        castList = soup.find("div",{'class':'castListWrapper'})
        castGroups = castList.findAll("dd",{'class':"dataBox3rd"})



        return ['fsdgfd','gfgfd']