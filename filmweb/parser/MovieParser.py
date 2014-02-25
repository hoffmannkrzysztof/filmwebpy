# coding=utf-8
import re
from bs4 import BeautifulSoup
from filmweb.Person import Person
from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.parser.ObjectParser import ObjectParser
from filmweb.func import get_text_or_none, get_datetime_or_none


class MovieParser(ObjectParser):

    def removeTag(self,soup, tagname):
        for tag in soup.findAll(tagname):
            contents = tag.contents
            parent = tag.parent
            tag.extract()


    def _parse_basic(self):
        dic = {}

        filmTitle = self.soup.find("div",{'class':"filmMainHeader"})
        title =  filmTitle.find('a')

        dic['title'] = get_text_or_none(title)

        year = filmTitle.find('span',{'id':'filmYear'})
        dic['year'] = get_text_or_none(year,'int')

        s = filmTitle.find('h2')
        #self.removeTag(s,"span")
        dic['title_original'] = get_text_or_none(s)

        desc = self.soup.find('div',{'class':"filmPlot"})
        dic['desc'] = get_text_or_none(desc)

        poster = self.soup.find('div',{'class':'posterLightbox'})
        if poster:
            p = poster.find("a")
            poster_img = p['href']
            dic['poster'] = poster_img
        else:
            dic['poster'] = None

        return dic
        
    def parse_genre(self):
        genres = [i.text for i in self.soup.find('div',{'class':'filmInfo'}).findAll('a') if 'genre' in i['href']]
        return genres

    def parse_real_url(self):
        if self.obj.objID and self.obj.url is None:
            return self.obj.get_url()

    def parse_episodes(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/episodes" )
        soup = BeautifulSoup(content)
        seasons = soup.findAll("table")
        episodeList = []
        for season in seasons:
            try:
                seasonNumber = season.find("h3").text.split()
                if seasonNumber[0] == 'sezon':
                    seasonNumber = int(seasonNumber[1])
                else:
                    seasonNumber = 0
            except:
                seasonNumber = 0

            episodes = season.findAll("td")
            for i in range(0, len(episodes), 3):

                number = episodes[i].text.split()
                if number[0] == 'odcinek':
                    number = int(number[1])
                else:
                    number = 0

                episodeDate = get_datetime_or_none(episodes[i+1].find('div'))
                episodeName = episodes[i+2].text
                episodeList.append({'season':seasonNumber, 'number':number, 'date':episodeDate, 'name': episodeName})
        return episodeList


    def parse_cast(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/cast" )
        soup = BeautifulSoup(content)
        castList = soup.find("div",{'class':'filmSubpageContentWrapper'})
        castGroups = castList.findAll(["dd","dt"])
        personList = []
        for cast in castGroups:
            if cast.name == 'dt':
                roleType = cast.text.split("/")[0].strip()
                roleType
            elif cast.name == 'dd':
                castList = cast.findAll("li")
                for person in castList:

                    try:
                        role = person.find("span",{'class':'roleName'}).text
                    except AttributeError:
                        role = None

                    name = person.find("span",{'class':'personName'}).text

                    patternlink = "/person/(.+)-(?P<id>[0-9]*)"
                    patternimg = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"

                    href = person.find("span",{'class':'personName'}).find("a")['href']

                    results = re.search(patternlink,href)
                    if results:
                        id = results.group("id")
                    else:
                        results = re.search(patternimg,unicode(person.extract()))
                        id = results.group("id")

                    personList.append( Person(id,title=name,roleType=roleType,roleName=role,url=href) )
        return personList

    def parse_additionalinfo(self):
        more_infos = []
        more_info = self.soup.find("div","pageBox sep-hr")
        more_info = more_info.find("dl")
        for more in more_info.findAll('dt'):
            if more.text != u'inne tytuły:':
                more_infos.append({'name': more.text.replace(":", ""), 'value': more.nextSibling.text})
        return more_infos

    def parse_basicinfo(self):
        basic_infos = []
        basic_info = self.soup.find("div","filmInfo")
        for basic in basic_info.findAll('th'):
                basic_infos.append({'name':basic.text,'value':basic.nextSibling.text})
        return basic_infos

    def parse_photos(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/photos" )
        soup = BeautifulSoup(content)
        photoList = soup.find("ul",'block-list photosList')
        images = []
        for photo in photoList.findAll("img"):
                images.append({'href':photo.parent['href'],'thumb':photo['src']})
        return images

    def parse_posters(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/posters" )
        soup = BeautifulSoup(content)
        photoList = soup.find("ul",'block-list postersList')
        images = []
        for photo in photoList("img",{'class':"lbProxy"}):
            images.append({'href':photo['src'].replace(".2.jpg",'.3.jpg'),'thumb':photo['src']})
        return images
