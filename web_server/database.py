import urllib.request
import json


class Config:
    couch_url = 'http://localhost:5984/social/'


class Couch:
    @staticmethod
    def Request(RequestAddress):
        url = Config.couch_url + RequestAddress
        response = urllib.request.urlopen(url).read().decode("utf-8")
        return json.loads(response)