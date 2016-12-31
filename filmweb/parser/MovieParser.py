# coding=utf-8
import datetime
import re

from bs4 import BeautifulSoup

from filmweb.Person import Person
from filmweb.func import get_text_or_none
from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.parser.ObjectParser import ObjectParser


class MovieParser(ObjectParser):
    def removeTag(self, soup, tagname):
        for tag in soup.findAll(tagname):
            contents = tag.contents
            parent = tag.parent
            tag.extract()


    def _parse_basic(self):
        dic = {}

        filmTitle = self.soup.find("div", {'class': "filmMainHeader"})
        title = filmTitle.find('a')

        dic['title'] = get_text_or_none(title)

        year = filmTitle.find('span', {'class': 'halfSize'})
        dic['year'] = get_text_or_none(year, 'int')

        s = filmTitle.find('h2')
        # self.removeTag(s,"span")
        dic['title_original'] = get_text_or_none(s)

        desc = self.soup.find('div', {'class': "filmPlot"})
        dic['desc'] = get_text_or_none(desc)

        poster = self.soup.find('div', {'class': 'posterLightbox'})
        if poster:
            p = poster.find("a")
            poster_img = p['href']
            dic['poster'] = poster_img
        else:
            dic['poster'] = None

        return dic

    def parse_genre(self):
        genres = [i.text for i in self.soup.find('div', {'class': 'filmInfo'}).findAll('a') if 'genre' in i['href']]
        return genres

    def parse_real_url(self):
        if self.obj.objID and self.obj.url is None:
            return self.obj.get_url()

    def parse_episodes(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve(self.obj.url + "/episodes")
        soup = BeautifulSoup(content)
        seasons = soup.find('dl', {'class': 'episodesTable'})
        episodes_list = []
        for element in seasons.children:
            if element.name == 'dt':
                h3 = element.next_element
                try:
                    season_number = int(h3.text.split(" ")[1])
                except:
                    break
            if element.name == 'dd':
                li_episodes = element.find_all("li")
                for episode in li_episodes:
                    episode_number = int(re.match(r'\d+', episode.contents[0].text).group())
                    date_str = episode.find('div',{'class':'countryPremiereDate'}).text
                    episode_name = episode.find('div',{'class':'title'}).text
                    episode_date = datetime.datetime.strptime(date_str,'%d.%m.%Y')

                    episodes_list.append({'season': season_number, 'number': episode_number, 'date': episode_date, 'name': episode_name})
        return episodes_list


    def parse_cast(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve(self.obj.url + "/cast/actors")
        soup = BeautifulSoup(content)
        cast_list_table = soup.find("table", {'class': 'filmCast'})
        cast_list = cast_list_table.find("tbody")


        personList = []
        for cast in cast_list_table.findAll('tr',id=re.compile("role_")):

            url_html = cast.find("a",{'class':'pImg49'})
            url = url_html['href']
            img_html = url_html.find("img")

            pattern_img = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"
            pattern_link = "/person/(.+)-(?P<id>[0-9]*)"



            results = re.search(pattern_link, url_html['href'])
            if results:
                id = results.group("id")
            else:
                results = re.search(pattern_img, repr(img_html.extract()))
                id = results.group("id")

            role_html  = cast.find('a',{'rel':'v:starring'})
            role = role_html.parent.nextSibling.nextSibling.text

            name = role_html.parent.nextSibling.text

            personList.append(Person(id, title=name, roleType='aktor', roleName=role, url=url))

            if cast.name == 'dt':
                roleType = cast.text.split("/")[0].strip()
                roleType
            elif cast.name == 'dd':
                castList = cast.findAll("li")
                for person in castList:

                    try:
                        role = person.find("span", {'class': 'roleName'}).text
                    except AttributeError:
                        role = None

                    name = person.find("span", {'class': 'personName'}).text

                    patternlink = "/person/(.+)-(?P<id>[0-9]*)"
                    patternimg = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"

                    href = person.find("span", {'class': 'personName'}).find("a")['href']

                    results = re.search(patternlink, href)
                    if results:
                        id = results.group("id")
                    else:
                        results = re.search(patternimg, repr(person.extract()))
                        id = results.group("id")

                    personList.append(Person(id, title=name, roleType=roleType, roleName=role, url=href))
        return personList

    def parse_additionalinfo(self):
        more_infos = []
        more_info = self.soup.find("div", {'class': "otherInfo"})
        more_info = more_info.find("dl")
        for more in more_info.findAll('dt'):
            if more.text not in(u'inne tytuły:',u'\xa0'):
                more_infos.append({'name': more.text.replace(":", ""), 'value': more.nextSibling.text})
        return more_infos

    def parse_basicinfo(self):
        basic_infos = []
        basic_info = self.soup.find("div", "filmInfo")
        for basic in basic_info.findAll('th'):
            if basic.text not in (u'\xa0',):
                basic_infos.append({'name': basic.text, 'value': basic.nextSibling.text})
        return basic_infos

    def parse_photos(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve(self.obj.url + "/photos")
        soup = BeautifulSoup(content)
        photos_list = soup.find("ul", {'class','photosList'})
        images = []
        for photo in photos_list.findAll("img"):
            images.append({'href': photo.parent['href'], 'thumb': photo['src'], 'image': photo.parent['data-photo']})
        return images

    def parse_posters(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve(self.obj.url + "/posters")
        soup = BeautifulSoup(content)
        photoList = soup.find("ul", 'block-list postersList')
        images = []
        for photo in photoList("img", {'class': "lbProxy"}):
            images.append({'href': photo['src'].replace(".2.jpg", '.3.jpg'), 'thumb': photo['src']})
        return images
