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
        t = self.soup.find('h1',{'class':'pageTitle'})
        title =  self.soup.find('h1',{'class':'pageTitle'})
        dic['title'] = get_text_or_none(title)

        year = self.soup.find('span',{'class':'filmYear'})
        dic['year'] = get_text_or_none(year,'int')

        s = self.soup.find('h2',{'class':'origTitle'})
        self.removeTag(s,"span")
        dic['title_original'] = get_text_or_none(s)

        desc = self.soup.find('span',{'class':"filmDescrBg"})
        dic['desc'] = desc

        poster = self.soup.find('a',{'class':'film_mini'})
        if poster:
            poster_img = poster['href']
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
        castList = soup.find("div",{'class':'castListWrapper'})
        castGroups = castList.findAll(["dd","dt"])
        personList = []
        for cast in castGroups:
            if cast['class'] == 'toggleUp':
                roleType = cast.text
                roleType = roleType.split("/")[0].strip()
            elif cast['class'] == 'dataBox3rd':
                castList = cast.findAll("li",id=re.compile("roleLine([0-9]*)"))
                for person in castList:
                    fields = person.findAll(["span","div"])
                    for field in fields:
                        if field.name == 'div':
                            role = field.text
                            if role:
                                role = role.replace("(","").replace(")","")
                        elif not field.has_key('class'):
                            name = field.text

                    patternlink = "/person/(.+)-(?P<id>[0-9]*)"
                    patternimg = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"

                    h3 = person.find("h3")
                    href = h3.find("a")['href']

                    results = re.search(patternlink,unicode(person.extract()))
                    if results:
                        id = results.group("id")
                    else:
                        results = re.search(patternimg,unicode(person.extract()))
                        id = results.group("id")
                    personList.append( Person(id,title=name,roleType=roleType,roleName=role,url=href) )
        return personList

    def parse_additionalinfo(self):
        more_infos = []
        more_info = self.soup.find("div","additional-info comBox")
        more_info = more_info.find("dl")
        for more in more_info.findAll('dt'):
            more_infos.append({'name':more.text.replace(":",""),'value':more.nextSibling.text})
        return more_infos

    def parse_basicinfo(self):
        basic_infos = []
        basic_info = self.soup.find("div","basic-info-wrapper")
        for basic in basic_info.findAll('th'):
                basic_infos.append({'name':basic.text,'value':basic.nextSibling.text})
        return basic_infos

    def parse_photos(self):
        grabber = HTMLGrabber()
        content = grabber.retrieve( self.obj.url+"/photos" )
        soup = BeautifulSoup(content,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )
        photoList = soup.find("div",{'class':'photosList comBox'})
        images = []
        for photo in photoList("a",{'class':"phNoImg2"}):
            images.append({'href':photo['href'],'thumb':photo.contents[1]['src']})
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