# coding=utf-8

class BaseObject(object):

    data = {}

    def set_data(self,data):
        """Set a data dictionary"""
        self.data.update(data)

    def set_title(self,title):
        if self.data.has_key('title'):
            self.title = self.data['title']
        else:
            title = title.split("/")[-1]
            self.title = title