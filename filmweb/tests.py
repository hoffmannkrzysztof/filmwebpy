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
        self.assertEqual( Levenshtein.distance(org_title,self.movie['title_original'].replace("The","")) , 3 )



class MovieNextTest(unittest.TestCase):
    def setUp(self):
        fw = Filmweb()
        self.movie = fw.get_movie(635169)

    def test_alllinkincast(self):
        for person in self.movie['cast']:
            self.assertNotEqual('http://www.filmweb.pl',person.url)
            self.assertIsNotNone(person.url)



class Movieparser(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.movie = self.fa.get_movie(671)

    def test_in(self):
        found_movies = self.fa.search_movie('Leon zawodowiec')
        self.assertTrue( self.movie in found_movies )

    def test_cast(self):
        self.assertIsNotNone( self.movie['cast'] )
        self.assertEqual(len(self.movie['cast']),100)

        p = self.movie['cast'][2]
        self.assertEqual(p['title'],u'Jean Reno')
        self.assertEqual(p['roleName'],u'Léon')
        self.assertEqual(p['roleType'],u'aktor')
        self.assertEqual(p.objID,88)

    def test_infos(self):
        self.assertEqual( len(self.movie['additionalinfo']), 4)

        self.assertEqual( len(self.movie['basicinfo']), 6)

        self.assertEqual( len(self.movie['photos']), 51 )

        self.assertEqual('Leon zawodowiec',self.movie.title,)
        #self.assertEqual('Léon',self.movie['title_original'],)

    def test_year(self):
        self.assertEqual( self.movie['year'], 1994)


class Osobaparser(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.osoba = self.fa.get_person(450)

    def test_infos(self):
        self.assertEqual('Kazimierz Kaczor',self.osoba.title,)
        self.assertEqual(self.osoba['birthdate'].month,2)
        self.assertEqual(self.osoba['birthdate'].day,9)
        self.assertEqual(self.osoba['birthdate'].year,1941)
        self.assertIsNotNone(self.osoba.get('poster'))


    def test_in(self):
        found_osoby = self.fa.search_person("Kazimierz Kaczor")
        self.assertTrue( self.osoba in found_osoby )

    def test_filmography(self):
        filmography = self.osoba['filmography']
        self.assertGreater(self.osoba['filmography'],0)

        film = filmography[0]
        self.assertEqual(film.objID,635169)

class PosterEmptyTest(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.osoba = self.fa.get_person(289000)

    def test_poster_and_name(self):
        self.assertIsNone(self.osoba.get('poster'))
        self.assertEqual(self.osoba['title'],u'David E. Browning')


class CanonicalnameTest(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.karewicz = self.fa.get_person(461) #Emil Karewicz
        self.kot = self.fa.get_person(148066) #tomasz kot
        self.zmuda =  self.fa.get_person(464409) #marta zmuda trzebiatowska
        self.niro =  self.fa.get_person(123) #Robert De Niro
        self.hopkins = self.fa.get_person(48) #Anthony Hopkins I

    def test_names(self):
        self.assertEqual(self.karewicz['canonicalname'],u'Karewicz Emil')
        self.assertEqual(self.kot['canonicalname'],u'Kot Tomasz')
        self.assertEqual(self.zmuda['canonicalname'],u'Żmuda-Trzebiatowska Marta')
        self.assertEqual(self.niro['canonicalname'],u'De Niro Robert')
        self.assertEqual(self.hopkins['canonicalname'],u'Hopkins I Anthony')



class NadZycieTest(unittest.TestCase):
    def setUp(self):
        self.fa = Filmweb('http')
        self.movie = self.fa.get_movie(651141)

    def test_cast(self):
        self.assertIsNotNone( self.movie['cast'] )
        p = self.movie['cast'][3]
        self.assertEqual(p['roleType'],u'aktor')

