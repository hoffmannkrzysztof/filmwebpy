# coding=utf-8
import urllib
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
        grabber = HTMLGrabber()
        p_title = grabber.encode_string(title)
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
        return Movie(movieID)

    def get_movie(self,movieID):
        return self._get_movie(movieID)

    def _get_real_id(self,*strings):
        for text in strings:
            text = str(text)

            list = re.findall("dropdownTarget ([0-9]*)_FILM", text)
            if len(list) and list[-1].isdigit():
                return int(list[-1])

            list =  re.findall(r'-([0-9]*)', text)
            if len(list) and list[-1].isdigit():
                return int(list[-1])

        return None

class ObjectParser(object):
    def __init__(self,obj):
        self.obj = obj
        if self.obj.url:
            self._download_content(self.obj.url)
            self.parse_basic()


    def _download_content(self,url):
        grabber = HTMLGrabber()
        self.content = grabber.retrieve(url)
        self.soup = BeautifulSoup(self.content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

    def parse_basic(self):
        self._parse_basic()

    def _parse_basic(self):
        """Parse basic information about movie or person. Eg. title, year, aka"""
        raise NotImplementedError('override this method')


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

    def encode_string(self,string):
        return urllib.quote(string.decode("utf8"))

    def open(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = self.get_headers()
        try:
            return opener.open(url)
        except urllib2.HTTPError, urllib2.URLError:
            raise FilmwebDataAccessError()

    def retrieve(self,url):
        return self.open(url).read()

