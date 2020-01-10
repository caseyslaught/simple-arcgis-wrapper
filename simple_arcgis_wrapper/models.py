'''

'''

class FeatureService(object):

    def __init__(self, id, name, url):
        self._id = id
        self._name = name
        self._url = url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url


class FeatureLayer(object):

    def __init__(self, id, name, url):
        self._id = id
        self._name = name
        self._url = url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

