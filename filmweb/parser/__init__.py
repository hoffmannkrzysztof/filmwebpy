# coding=utf-8
import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from filmweb.Movie import Movie
from filmweb.Person import Person
from filmweb._exceptions import FilmwebDataAccessError
from filmweb.vars import filmweb_movie_search, filmweb_person_link
import re, htmlentitydefs

class FilmwebHTTP(object):

    def _search_movie(self,title,results):
        """Return list of movies"""
        p_title = title #@TODO Convert to ascii
        grabber = HTMLGrabber()
        li_list = []

        for type in ['film','serial']:
            content = grabber.retrieve(filmweb_movie_search % (type,p_title,1)) #@Make search more pages not only 1
            soup=BeautifulStoneSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
            li_list.extend( soup.findAll('li',{'class':'searchResult'}) )

        for li in li_list:
            a = li.find('a',{'class':'searchResultTitle'})
            title = a.text
            url = a['href']
            # have to do another check because sometimes url doesnt provide movieID
            div = li.find('div',{'class': re.compile(r'\bdropdownTarget\b')})

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
        Movie(movieID,title=title)

    def _get_real_id(self,*strings):
        for text in strings:
            text = str(text)

            list =  re.findall(r'-([0-9]*)', text)
            if len(list) and list[-1].isdigit():
                return int(list[-1])

            list = re.findall("dropdownTarget ([0-9]*)_FILM", text)
            if len(list) and list[-1].isdigit():
                return int(list[-1])

        return None



class HTMLGrabber(object):
    def __init__(self, *args, **kwargs):
        self.headers = []
        self.set_header('User-agent', 'Googlebot/2.1 (+http://www.google.com/bot.html)')
        self.set_header('Referer', 'http://www.filmweb.pl/')
        self.set_header('Cookie', 'welcomeScreenNew=welcomeScreen')

    def set_header(self, header, value):
        """Set a header."""
        self.headers.append((header, value))

    def get_headers(self):
        return self.headers

    def retrieve(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = self.get_headers()
        try:
            f = opener.open(url)
        except urllib2.HTTPError, urllib2.URLError:
            raise FilmwebDataAccessError()
        else:
            return f.read()