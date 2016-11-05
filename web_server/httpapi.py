import urllib.request
import json

from config import Config




class HttpApi:

    @staticmethod
    def GetDB(url):
        urlFull = Config.couchDbUrl + url
        response = urllib.request.urlopen(urlFull).read().decode("utf-8")
        return json.loads(response)

    @staticmethod
    def Get(url):
        response = urllib.request.urlopen(url).read().decode("utf-8")
        return json.loads(response)

    @staticmethod
    def PostDB(url, data):
        url_full = Config.couchDbUrl + url
        data = bytes(data.encode("utf-8"))
        req = urllib.request.Request(url_full, data, headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req)




