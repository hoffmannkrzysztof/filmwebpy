# coding=utf-8
import unittest
from filmweb import Filmweb


class Movieparser(unittest.TestCase):
    def setUp(self):
        fa = Filmweb('http')
        self.found_movies = fa.search_movie('Leon zawodowiec')
        self.movie = fa.get_movie(671)

    def test_isMovieFound(self):
        self.assertTrue( self.movie in self.found_movies )

    def test_additionalinfo(self):
        self.assertEqual( len(self.movie['additionalinfo']), 4)

    def test_basicinfo(self):
        self.assertEqual( len(self.movie['basicinfo']), 6)

    def test_photos(self):
        self.assertEqual( len(self.movie['photos']), 51 )

    def test_default_ingo(self):
        self.assertEqual('Leon zawodowiec',self.movie.title,)
        self.assertEqual('Léon',self.movie['title_original'],)
        #self.assertEqual(self['movie']['desc'],'Leon zawodowiec')

