# coding=utf-8
import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from filmweb.Movie import Movie
from filmweb._exceptions import FilmwebDataAccessError
from filmweb.vars import filmweb_film_search
import re, htmlentitydefs

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

class FilmwebHTTP(object):

    def _search_movie(self,title,results):
        """Return list of movies"""
        p_title = title #@TODO Convert to ascii
        grabber = HTMLGrabber()
        content = grabber.retrieve(filmweb_film_search % (p_title,1)) #@Make search more pages not only 1
        soup=BeautifulStoneSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        for li in soup.findAll('li',{'class':'searchResult'}):
            a = li.find('a',{'class':'searchResultTitle'})
            title = a.text

            movieID = self._get_real_id(a['href'])
            if not movieID: # have to do another check because sometimes url doesnt provide movieID
                div = li.find('div',{'class': re.compile(r'\bdropdownTarget\b')})
                movieID = self._get_real_id(div['class'])

            yield movieID,title

    def search_movie(self,title,results=20):
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [ Movie(movieID,title) for movieID,title in self._search_movie(title,results) ]

    def _search_person(self,name,results=None):
        #http://www.filmweb.pl/search/person?q=Tom+Cruise
        """Return list of persons"""

    def _get_person(self,personID):
        """Return Person object"""

    def _get_movie(self,movieID):
        """Return Movie object"""

    def _get_real_id(self,text):
        if text:
            text = str(text)
            link_re = r'-([0-9]*)'
            dropclass_re = "dropdownTarget ([0-9]*)_FILM"

            try:
                last = re.findall(link_re, text)
                return int(last[-1])
            except Exception,e:
                print e

            try:
                last = re.findall(dropclass_re, text)
                return int(last[-1])
            except Exception,e:
                print e

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