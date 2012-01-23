# coding=utf-8
from urlparse import urljoin
from filmweb.vars import filmweb_root


class BaseObject(object):

    def __init__(self,objID,title=None,url=None,data=None,roleType=None,roleName=None):
        self.reset()
        if data is None: data = {}
        self.set_id(objID)
        self.set_data(data)
        self.set_title(title)
        self.set_url(url)
        self.roleName = roleName
        self.roleType = roleType


    def reset(self):
        self.data = {}
        self.objID = None
        self.title = u''
        self.url = u''
        self.attr = u''

    def __getitem__(self, key):
        """Return the value for a given key"""

        if self.data.has_key(key):
            return self.data[key]
        else:
            classname = str(self.__class__.__name__)+"Parser"
            exec "from filmweb.parser."+classname+" import "+classname #too hacky!
            obj = locals()[classname](self)
            method = getattr(obj, 'parse_'+key)
            self[key] = method()
            return self[key]

    def __setitem__(self, key, item):
        """Store the item with the given key."""
        self.data[key] = item

    def __delitem__(self, key):
        """Remove the given key."""
        del self.data[key]

    def set_data(self,data):
        """Set a data dictionary"""
        self.data.update(data)

    def set_url(self,url):
        if url is not None:
            self.url = urljoin(filmweb_root,url).strip()

    def set_id(self,id):
        self.objID = int(id)

    def set_title(self,title):
        if self.data.has_key('title'):
            self.title = self.data['title']
        else:
            title = title.split("/")[-1]
            self.title = title
        self.title = self.title.strip()

    def isSame(self,item):
        return self.objID == self.objID