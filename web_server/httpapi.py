import urllib.request
import json

from config import Config




class HttpApi:

    @staticmethod
    def Get(url):
        url_full = Config.couchUrl + url
        response = urllib.request.urlopen(url_full).read().decode("utf-8")
        return json.loads(response)

    @staticmethod
    def Post(url, data):
        url_full = Config.couchUrl + url
        data = bytes(data.encode("utf-8"))
        req = urllib.request.Request(url_full, data, headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req)




