# coding=utf-8
import re

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode

from bs4 import BeautifulSoup

from filmweb.Movie import Movie
from filmweb.Person import Person
from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.vars import filmweb_search_blank
from filmweb.vars import filmweb_person_search
from filmweb.func import get_real_id


class FilmwebHTTP(object):
    def _search_movie(self, title, results, genre_id, search_type, start_year, end_year):
        """Return list of movies"""
        grabber = HTMLGrabber()
        li_list = []
        img_list = []
        params = {"q": title.encode("utf-8"), "page": 1}
        if genre_id: params['genreIds'] = genre_id
        if start_year: params['startYear'] = start_year
        if end_year: params['endYear'] = end_year

        search_url = ""
        if search_type:
            search_url = "/" + search_type

        url = filmweb_search_blank + search_url + "?" + urlencode(params)

        content = grabber.retrieve(url)  # @Make search more pages not only 1
        soup = BeautifulSoup(content)
        li_list.extend(soup.findAll('div', {'class': 'hitDescWrapper'}))
        img_list.extend(soup.findAll('div', {'class': 'hitImage'}))

        for i, li in enumerate(li_list):
            a = li.find('a', {'class': 'hdr hdr-medium hitTitle'})
            title = a.text
            url = a['href']
            # have to do another check because sometimes url doesnt provide movieID
            aimg = img_list[i].find('a')
            if aimg is not None:
                img = aimg.find("img")
                movieID = get_real_id(url, img['src'])
                yield movieID, title, url

    def search_movie(self, title, results=20, genre_id=None, search_type=None, start_year=None, end_year=None):
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [Movie(objID=movieID, title=title, url=url) for movieID, title, url in
                self._search_movie(title, results, genre_id, search_type, start_year, end_year)]

    def _search_person(self, title, results=20):
        # http://www.filmweb.pl/search/person?q=Tom+Cruise
        """Return list of persons"""
        grabber = HTMLGrabber()
        p_title = grabber.encode_string(title)
        li_list = []
        img_list = []

        content = grabber.retrieve(filmweb_person_search % (p_title, 1))  #@Make search more pages not only 1
        soup = BeautifulSoup(content)
        li_list.extend(soup.findAll('div', {'class': 'hitDescWrapper'}))
        img_list.extend(soup.findAll('div', {'class': 'hitImage'}))

        for i, li in enumerate(li_list):
            a = li.find('a', {'class': 'hdr hdr-medium hitTitle'})
            title = a.text
            url = a['href']
            # have to do another check because sometimes url doesnt provide movieID
            aimg = img_list[i].find('a')
            if aimg is not None:
                img = aimg.find('img')
                personID = get_real_id(url, img['src'])
                yield personID, title, url

    def search_person(self, title, results=20):
        """Return list of persons"""
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [Person(objID=personID, title=title, url=url) for personID, title, url in
                self._search_person(title, results)]

    def get_person(self, personID):
        return self._get_person(personID)

    def _get_person(self, personID):
        """Return Person object"""
        return Person(personID)

    def _get_movie(self, movieID):
        """Return Movie object"""
        return Movie(movieID)

    def get_movie(self, movieID):
        return self._get_movie(movieID)