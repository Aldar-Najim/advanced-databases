import urllib.request
import json


class Config:
    couch_url = 'http://localhost:5984/social/'


class Couch:
    @staticmethod
    def Get(url):
        url_full = Config.couch_url + url
        response = urllib.request.urlopen(url_full).read().decode("utf-8")
        return json.loads(response)

    @staticmethod
    def Post(url, data):
        url_full = Config.couch_url + url
        data = bytes(data.encode("utf-8"))
        req = urllib.request.Request(url_full, data, headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req)




