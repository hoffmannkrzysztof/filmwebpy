# coding=utf-8
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
from filmweb.Person import Person
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
        castGroups = castList.findAll(["dd","dt"])
        personList = []
        for cast in castGroups:
            if cast['class'] == 'toggleUp':
                roleType = cast.text
            elif cast['class'] == 'dataBox3rd':
                castList = cast.findAll("li",id=re.compile("roleLine([0-9]*)"))
                for person in castList:
                    fields = person.findAll(["span","div"])
                    for field in fields:
                        if field.name == 'div':
                            role = field.text
                        elif not field.has_key('class'):
                            name = field.text

                    patternlink = "/person/(.+)-(?P<id>[0-9]*)"
                    patternimg = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"

                    results = re.search(patternlink,unicode(person.extract()))
                    if results:
                        id = results.group("id")
                    else:
                        results = re.search(patternimg,unicode(person.extract()))
                        id = results.group("id")
                    personList.append( Person(id,title=name,roleType=roleType,roleName=role) )



        return personList