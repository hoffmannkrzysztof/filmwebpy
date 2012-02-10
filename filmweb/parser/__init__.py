# coding=utf-8

from BeautifulSoup import BeautifulStoneSoup
from filmweb.Movie import Movie
from filmweb.Person import Person
from filmweb.vars import filmweb_movie_search, filmweb_person_link
import re
from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.vars import filmweb_search

class FilmwebHTTP(object):

    def _search_movie(self,title,results,):
        """Return list of movies"""
        grabber = HTMLGrabber()
        p_title = grabber.encode_string(title)
        li_list = []

        #for type in ['film','serial']:
        content = grabber.retrieve(filmweb_search % (p_title,1)) #@Make search more pages not only 1
        soup=BeautifulStoneSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        li_list.extend( soup.findAll('li',{'class':'searchResult'}) )

        for li in li_list:
            a = li.find('a',{'class':'searchResultTitle'})
            title = a.text
            url = a['href']
            # have to do another check because sometimes url doesnt provide movieID
            div = li.find('div',{'class': re.compile(r'\bdropdownTarget\b')})
            if div is not None:
                movieID = self._get_real_id(url,div['class'])
                yield movieID,title,url

    def search_movie(self,title,results=20):
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [ Movie(objID=movieID,title=title,url=url) for movieID,title,url in self._search_movie(title,results) ]

    def _search_person(self,name,results=None):
        #http://www.filmweb.pl/search/person?q=Tom+Cruise
        """Return list of persons"""

    def get_person(self,personID):
        return self._get_person(personID)

    def _get_person(self,personID):
        """Return Person object"""
        grabber = HTMLGrabber()
        content = grabber.retrieve(filmweb_person_link % ("",personID))
        soup = BeautifulStoneSoup( content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        title = soup.find("h1",{'class':'pageTitle'}).text
        return Person(personID,title=title)

    def _get_movie(self,movieID):
        """Return Movie object"""
        return Movie(movieID)


    def get_movie(self,movieID):
        return self._get_movie(movieID)

    def _get_real_id(self,*strings):
        for text in strings:
            text = str(text)

            found = re.search("dropdownTarget (?P<id>[0-9]*)_(FILM|SERIAL)", text)
            if found is not None:
                return int(found.group('id'))

            list =  re.findall(r'-([0-9]*)', text)
            if len(list) and list[-1].isdigit():
                return int(list[-1])

        return None