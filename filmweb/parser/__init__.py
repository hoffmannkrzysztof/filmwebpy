# coding=utf-8
import re

from BeautifulSoup import BeautifulStoneSoup
from filmweb.Movie import Movie
from filmweb.Person import Person
from filmweb.vars import filmweb_movie_search, filmweb_person_link

from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.vars import filmweb_search
from filmweb.vars import filmweb_person_search
from filmweb.func import get_real_id

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
            aimg = li.find('a',{'class': 'fNoImg25'})
            if aimg is not None:
                img = aimg.find("img")
                movieID = get_real_id(url,img['src'])
                yield movieID,title,url

    def search_movie(self,title,results=20):
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [ Movie(objID=movieID,title=title,url=url) for movieID,title,url in self._search_movie(title,results) ]

    def _search_person(self,title,results=20):
        #http://www.filmweb.pl/search/person?q=Tom+Cruise
        """Return list of persons"""
        grabber = HTMLGrabber()
        p_title = grabber.encode_string(title)
        li_list = []

        content = grabber.retrieve(filmweb_person_search % (p_title,1)) #@Make search more pages not only 1
        soup=BeautifulStoneSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        li_list.extend( soup.findAll('li',{'class':'searchResult'}) )

        for li in li_list:
            a = li.find('a',{'class':'searchResultTitle'})
            title = a.text
            url = a['href']
            # have to do another check because sometimes url doesnt provide movieID
            aimg = li.find('a',{'class': 'pNoImg3'})
            if aimg is not None:
                img = aimg.find('img')
                personID = get_real_id(url,img['src'])
                yield personID,title,url

    def search_person(self,title,results=20):
        """Return list of persons"""
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [ Person(objID=personID,title=title,url=url) for personID,title,url in self._search_person(title,results) ]

    def get_person(self,personID):
        return self._get_person(personID)

    def _get_person(self,personID):
        """Return Person object"""
        return Person(personID)

    def _get_movie(self,movieID):
        """Return Movie object"""
        return Movie(movieID)

    def get_movie(self,movieID):
        return self._get_movie(movieID)