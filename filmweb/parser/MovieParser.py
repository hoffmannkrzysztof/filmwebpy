# coding=utf-8
import re
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
from filmweb.Person import Person
from filmweb.parser.HTMLGrabber import HTMLGrabber
from filmweb.parser.ObjectParser import ObjectParser
from filmweb.func import get_text_or_none


class MovieParser(ObjectParser):

    def removeTag(self,soup, tagname):
        for tag in soup.findAll(tagname):
            contents = tag.contents
            parent = tag.parent
            tag.extract()


    def _parse_basic(self):
        dic = {}

        filmTitle = self.soup.find("div",{'class':"filmTitle"})


        title =  filmTitle.find('h1')
        dic['title'] = get_text_or_none(title)

        year = filmTitle.find('span',{'id':'filmYear'})
        dic['year'] = get_text_or_none(year,'int')

        s = filmTitle.find('h2')
        #self.removeTag(s,"span")
        dic['title_original'] = get_text_or_none(s)

        desc = self.soup.find('span',{'class':"filmPlot"})
        dic['desc'] = desc

        poster = self.soup.find('div',{'class':'posterLightbox'})
        if poster:
            p = poster.find("a")
            poster_img = p['href']
            dic['poster'] = poster_img
        else:
            dic['poster'] = None

        return dic

    def parse_real_url(self):
        if self.obj.objID and self.obj.url is None:
            return self.obj.get_url()

    def parse_cast(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/cast" )
        soup = BeautifulSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
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
            more_infos.append({'name':more.text.replace(":",""),'value':more.nextSibling.text})
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
        soup = BeautifulSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        photoList = soup.find("ul",'block-list photosList')
        images = []
        for photo in photoList.findAll("img"):
                images.append({'href':photo.parent['href'],'thumb':photo['src']})
        return images

    def parse_posters(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/posters" )
        soup = BeautifulSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        photoList = soup.find("div",{'class':'posters comBox'})
        images = []
        for photo in photoList("img",{'class':"lbProxy"}):
            images.append({'href':photo['src'].replace(".2.jpg",'.3.jpg'),'thumb':photo['src']})
        return images