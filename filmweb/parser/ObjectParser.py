# coding=utf-8
from bs4 import BeautifulSoup


class ObjectParser(object):
    _soup = None
    _content = None

    def __init__(self, obj):
        self.obj = obj

    @property
    def content(self):
        if self._content is None:
            self._download_content(self.obj.url)
        return self._content

    @property
    def soup(self):
        if self._soup is None:
            self._download_content(self.obj.url)
        return self._soup

    def _download_content(self, url):
        from filmweb.parser.HTMLGrabber import HTMLGrabber

        grabber = HTMLGrabber()
        self._content = grabber.retrieve(url)
        self._soup = BeautifulSoup(self.content)

    def parse_basic(self):
        return self._parse_basic()

    def _parse_basic(self):
        """Parse basic information about movie or person. Eg. title, year, aka"""
        raise NotImplementedError('override this method')