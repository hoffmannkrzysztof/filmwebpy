# coding=utf-8

filmweb_root = 'http://www.filmweb.pl'

filmweb_movie_link = filmweb_root + "/film/%s-%d-%d"  # name,year,id
filmweb_person_link = filmweb_root + "/person/%s-%d"  # name,id

filmweb_search_blank = filmweb_root + '/search'
filmweb_search = filmweb_root + '/search?q=%s&page=%d'
filmweb_movie_search = filmweb_root + "/search/%s?q=%s&page=%d&genreIds="
filmweb_person_search = filmweb_root + "/search/person?q=%s&page=%d"

filmweb_person_link = filmweb_root + "/person/%s-%d"