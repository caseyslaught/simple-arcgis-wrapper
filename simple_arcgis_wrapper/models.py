
import urllib.parse


class FeatureService(object):
    def __init__(self, id, name, title, url):
        self._id = id
        self._name = name
        self._title = title
        self._url = urllib.parse.quote(url, safe="%/:?=&")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    # update in AGOL, will need to pass api to model
    #@title.setter
    #def title(self, title):
    #    self._title = title

    @property
    def url(self):
        return self._url

    # Or maybe include a .save method which 
    # pushes all changes to AGOL


class FeatureLayer(object):
    def __init__(self, id, name, url):
        self._id = id
        self._name = name
        self._url = urllib.parse.quote(url, safe="%/:?=&")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url


class PointFeature(object):
    def __init__(self, id, x, y):
        self._id = id
        self._x = x
        self._y = y

    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
