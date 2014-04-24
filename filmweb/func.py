# coding=utf-8
import re
from datetime import datetime

from bs4 import BeautifulSoup

from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.vars import filmweb_search_blank


def get_real_id(*strings):
    for text in strings:
        text = str(text)

        found = re.search(
            "http://([0-9]{1,2}).fwcdn.pl/(p|po)/([0-9]{1,4})/([0-9]{1,4})/(?P<id>[0-9]{1,9})/([0-9]{1,9}).([0-9]{1}).jpg",
            text)
        if found is not None:
            return int(found.group('id'))

        found = re.search("dropdownTarget (?P<id>[0-9]*)_(FILM|SERIAL)", text)
        if found is not None:
            return int(found.group('id'))

        list = re.findall(r'-([0-9]*)', text)
        if len(list) and list[-1].isdigit():
            return int(list[-1])

    return 0


def get_canonical_name(title):
    splited = title.split(" ")
    name = splited[0]
    surname = splited[1:]
    surname.extend([name])

    return " ".join(surname)


def get_text_or_none(var, typ='str'):
    if typ == 'int':
        try:
            t = var.text[var.text.find('(') + 1:var.text.find(')')]
            return t
        except:
            return ''
    else:
        try:
            return var.text
        except:
            return ''


def get_datetime_or_none(txt):
    MONTHS = {u'stycznia': 1, u'lutego': 2, u'marca': 3, u'kwietnia': 4, u'maja': 5, u'czerwca': 6,
              u'lipca': 7, u'sierpnia': 8, u'września': 9, u'października': 10, u'listopada': 11, u'grudnia': 12
    }
    try:
        list = txt.text.split()
        month = MONTHS[list[1]]
        return datetime.strptime("%s-%d-%s" % (list[2], month, list[0]), "%Y-%m-%d")
    except:
        return None


def get_list_genres():
    grabber = HTMLGrabber()
    content = grabber.retrieve(filmweb_search_blank + "/film")
    soup = BeautifulSoup(content)
    genres = soup.findAll('input', {'name': 'genreIds'})
    list_genre = []
    for genre in genres:
        genre_id = genre.attrs['value']
        genre_name = genre.next_element.next_element.text
        list_genre.append({'genre_id': genre_id, 'genre_name': genre_name})
    return list_genre



