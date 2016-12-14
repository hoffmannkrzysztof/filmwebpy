# coding=utf-8
import datetime

from filmweb.parser.ObjectParser import ObjectParser
from filmweb.func import get_real_id
from filmweb.func import get_canonical_name


class PersonParser(ObjectParser):
    def _parse_basic(self):
        dic = {}

        poster = self.soup.find("img", "personBigPhoto")
        if poster['src'].find("plug.svg") == -1:
            dic['poster'] = poster['src']
        else:
            dic['poster'] = None

        title = poster['alt'].strip()
        dic['title'] = title
        dic['canonicalname'] = get_canonical_name(dic['title'])

        more_info = self.soup.find("div", "personInfo")

        if more_info:
            for more in more_info.findAll('tr'):
                name = more.find('th')
                value = more.find('td')
                js = value.find('script')
                if js:
                    js.extract()
                dic[name.text.replace(":", "")] = value.text

            if dic.get('data urodzenia', None):
                try:
                    dic['birthdate'] = datetime.datetime.strptime(dic['data urodzenia'], "%Y-%m-%d")  # 1923-03-13
                except ValueError:
                    dic['birthdate'] = None

            if dic.get('data śmierci', None):
                try:
                    dic['deaddate'] = datetime.strptime(dic['data śmierci'], "%Y-%m-%d")
                except ValueError:
                    dic['deaddate'] = None
        return dic

    def parse_filmography(self):
        from filmweb.Movie import Movie

        movie_links = self.soup.findAll("tr", {'data-type': "F"})

        movies = []
        for movie_link in movie_links:
            a = movie_link.find("a")
            movieID = get_real_id(a['href'])
            movies.append(Movie(objID=movieID, title=a.text, url=a['href']))
        return movies

