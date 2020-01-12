'''

'''

import urllib.parse

class FeatureService(object):

    def __init__(self, id, name, title, url):
        self._id = id
        self._name = name
        self._title = title
        self._url = urllib.parse.quote(url, safe='%/:?=&')

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url


class FeatureLayer(object):

    def __init__(self, id, name, url):
        self._id = id
        self._name = name
        self._url = urllib.parse.quote(url, safe='%/:?=&')

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url


class Feature(object):

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id