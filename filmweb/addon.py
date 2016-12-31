# coding=utf-8
try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

from filmweb.vars import filmweb_root


class BaseObject(object):
    def __init__(self, objID, title=None, url=None, roleType=None, roleName=None):
        self.reset()
        self.set_id(objID)
        self.set_url(url)
        self.parser_obj = self.parser()
        self.set_title(title)

        self['roleName'] = roleName
        self['roleType'] = roleType

    def reset(self):
        self.data = {}
        self.objID = None
        self.title = None
        self.url = None

    def get(self, key, default=None):
        try:
            if self[key]:
                return self[key]
            else:
                return default
        except:
            return default

    def __getitem__(self, key):
        """Return the value for a given key"""

        if key in self.data:
            return self.data[key]
        else:

            if key in ('title', 'year', 'title_original', 'desc', 'poster', 'birthdate', 'deaddate', 'canonicalname'):
                dic = self.parser_obj.parse_basic()
                self.set_data(dic)
            elif key == 'url':
                self[key] = self.parser_obj.parse_real_url()
            else:
                method = getattr(self.parser_obj, 'parse_' + key)
                self[key] = method()
            return self.data[key]

    def __setitem__(self, key, item):
        """Store the item with the given key."""
        self.data[key] = item

    def __delitem__(self, key):
        """Remove the given key."""
        del self.data[key]

    def __eq__(self, other):
        return self.objID == other.objID

    def parser(self):
        return self._parser()

    def set_data(self, data):
        self.data.update(data)

    def set_url(self, url):
        if url is not None:
            self.url = urljoin(filmweb_root, url).strip()
        else:
            self.url = self.get_url()

    def _get_url(self):
        """Return movie, person url"""
        raise NotImplementedError('override this method')

    def get_url(self):
        if self.url:
            return self.url
        else:
            return self._get_url()

    def set_id(self, id):
        self.objID = int(id)

    def set_title(self, title):
        if title is not None:
            title = title.split("/")[0]
            self.title = title
        else:
            self.title = self['title']

        self.title = self.title.strip()
        self['title'] = self.title

    def isSame(self, item):
        return self.objID == self.objID