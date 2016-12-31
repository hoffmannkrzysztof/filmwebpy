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
    def _search_movie(self, title, results):
        """Return list of movies"""
        grabber = HTMLGrabber()
        li_list = []
        img_list = []
        params = {"q": title.encode("utf-8"), "page": 1}

        url = filmweb_search_blank + "?" + urlencode(params)

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

    def search_movie(self, title, results=20, ):
        try:
            results = int(results)
        except ValueError:
            results = 20

        return [Movie(objID=movieID, title=title, url=url) for movieID, title, url in
                self._search_movie(title, results, )]

    def search_filtered_movie(self, title=None, results=20, genre_id=None, search_type=None):
        if search_type not in ['film', 'serial']:
            search_type = None

        return [Movie(objID=movieID, title=title, url=url) for movieID, title, url in
                self._search_filtered_movie(title, results, genre_id, search_type)]

    def _search_filtered_movie(self, title, results, genre_id, search_type):

        grabber = HTMLGrabber()
        params = {}
        params['page'] = 1
        if title: params['q'] = title.encode("utf-8")
        if genre_id: params['genreIds'] = genre_id

        search_url = ""
        if search_type:
            search_url = "/" + search_type

        url = filmweb_search_blank + search_url + "?" + urllib.urlencode(params)

        content = grabber.retrieve(url)
        soup = BeautifulSoup(content)
        hits = soup.findAll('li', {'id': re.compile('hit_([0-9]*)')})
        for hit in hits:
            h3 = hit.find("h3")
            url = h3.find("a")['href']
            div_img = hit.find("div", {'class': 'filmPoster-1'})
            img = div_img.find("img")
            movieID = get_real_id(url, img['src'])

            yield movieID, title, url


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