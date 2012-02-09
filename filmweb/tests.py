# coding=utf-8
import unittest
from filmweb import Filmweb
import Levenshtein


class Serialparser(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.serial = self.fa.get_movie(33993)

    def test_in(self):
        found_movies = self.fa.search_movie('Przyjaciele')
        self.assertTrue( self.serial in found_movies )

    def test_year(self):
        self.assertEqual( self.serial['year'], '1994 - 2004')




class CheckMovieInfos(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.movie = self.fa.get_movie(107552)

    def test_in(self):
        found_movies = self.fa.search_movie(u'Dziewczyna z sąsiedztwa')
        self.assertTrue( self.movie in found_movies )

    def test_levenstein(self):
        org_title = u'The Girl Next Door'.replace("The","")
        self.assertEqual('Girl Next Door, The',self.movie['title_original'])
        self.assertEqual( Levenshtein.distance(org_title,self.movie['title_original'].replace("The","")) , 2 )





class Movieparser(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.movie = self.fa.get_movie(671)

    def test_in(self):
        found_movies = self.fa.search_movie('Leon zawodowiec')
        self.assertTrue( self.movie in found_movies )

    def test_infos(self):
        self.assertEqual( len(self.movie['additionalinfo']), 4)

        self.assertEqual( len(self.movie['basicinfo']), 6)

        self.assertEqual( len(self.movie['photos']), 51 )

        self.assertEqual('Leon zawodowiec',self.movie.title,)
        #self.assertEqual('Léon',self.movie['title_original'],)

    def test_year(self):
        self.assertEqual( self.movie['year'], 1994)



