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
        self.title = None
        self.url = None
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

    def __eq__(self, other):
        return self.objID == other.objID

    def set_data(self,data):
        """Set a data dictionary"""
        self.data.update(data)

    def set_url(self,url):
        if url is not None:
            self.url = urljoin(filmweb_root,url).strip()
        elif self.objID:
            self.url = self.get_url()

    def _get_url(self):
        """Return movie, person url"""
        raise NotImplementedError('override this method')

    def get_url(self):
        return self._get_url()

    def set_id(self,id):
        self.objID = int(id)

    def set_title(self,title):
        if self.data.has_key('title'):
            self.title = self.data['title']
        elif title is not None:
            title = title.split("/")[-1]
            self.title = title
        else:
            self.title = "Not found yet"

        self.title = self.title.strip()

    def isSame(self,item):
        return self.objID == self.objID