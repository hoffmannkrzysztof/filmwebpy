# coding=utf-8

from filmweb.parser.ObjectParser import ObjectParser
from filmweb.func import get_real_id
from dateutil import parser
from filmweb.func import get_text_or_none,canonicalname

class PersonParser(ObjectParser):



    def _parse_basic(self):
        dic = {}

        title =  self.soup.find('h1',{'class':'pageTitle'})
        dic['title'] = get_text_or_none(title)
        dic['canonicalname'] = canonicalname(dic['title'])

        more_info = self.soup.find("div","additional-info comBox")

        if more_info:
            more_info = more_info.find("dl")
            for more in more_info.findAll('dt'):
                dic[ more.text.replace(":","") ] = more.nextSibling.text

            if dic.get('data urodzenia',None):
                dic['birthdate'] = parser.parse(dic['data urodzenia'])

            if dic.get('data śmierci',None):
                dic['deaddate'] = parser.parse(dic['data śmierci'])


        poster = self.soup.find("img","personBigPhoto")
        if poster is not None:
            if poster['src'].find("NoImg") == -1:
                dic['poster'] = poster['src']

        return dic

    def parse_filmography(self):
        from filmweb.Movie import Movie
        movie_links = self.soup.findAll("a","filmographyFilmTitle")
        movies = []
        for a in movie_links:
            movieID = get_real_id(a['href'])
            movies.append( Movie(objID=movieID,title=a.text,url=a['href']) )
        return movies

