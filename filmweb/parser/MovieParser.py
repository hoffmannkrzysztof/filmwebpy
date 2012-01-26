# coding=utf-8
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
from filmweb.Person import Person
from filmweb.parser import HTMLGrabber, ObjectParser
from filmweb.vars import filmweb_root

class MovieParser(ObjectParser):


    def removeTag(self,soup, tagname):
        for tag in soup.findAll(tagname):
            contents = tag.contents
            parent = tag.parent
            tag.extract()

    def _parse_basic(self):

        title =  self.soup.find('h1',{'class':'pageTitle'}).text
        self.obj.set_title(title)
        self.obj['title'] = title


        year = self.soup.find('span',{'class':'filmYear'}).text
        self.obj['year'] = year

        s = self.soup.find('h2',{'class':'origTitle'})
        self.removeTag(s,"span")
        title_original = s.text
        self.obj['title_original'] = title_original

        desc = self.soup.find('span',{'class':"filmDescrBg"}).text
        self.obj['desc'] = desc

        poster = self.soup.find('a',{'class':'film_mini'})
        poster_img = poster['href']
        self.obj['poster'] = poster_img


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
            elif cast['class'] == 'dataBox3rd':
                castList = cast.findAll("li",id=re.compile("roleLine([0-9]*)"))
                for person in castList:
                    fields = person.findAll(["span","div"])
                    for field in fields:
                        if field.name == 'div':
                            role = field.text
                        elif not field.has_key('class'):
                            name = field.text

                    patternlink = "/person/(.+)-(?P<id>[0-9]*)"
                    patternimg = "http://1.fwcdn.pl/p/([0-9]{2})/([0-9]{2})/(?P<id>[0-9]*)/([0-9]*).([0-3]*).jpg"

                    results = re.search(patternlink,unicode(person.extract()))
                    if results:
                        id = results.group("id")
                    else:
                        results = re.search(patternimg,unicode(person.extract()))
                        id = results.group("id")
                    personList.append( Person(id,title=name,roleType=roleType,roleName=role) )
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