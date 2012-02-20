# coding=utf-8
from filmweb._exceptions import FilmwebDataAccessError
import urllib
import urllib2

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
        return urllib.quote(string.encode("utf-8"))

    def open(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = self.get_headers()
        try:
            return opener.open(url)
        except urllib2.HTTPError, urllib2.URLError:
            raise FilmwebDataAccessError()
        except ValueError:
            pass

    def retrieve(self,url):
        return self.open(url).read()