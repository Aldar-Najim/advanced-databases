import json

from httpapi import HttpApi
from config import Config


# this class handles different database requests using HttpApi

class Requests:

    @staticmethod
    def ExtractRows(parsed):
        rows = parsed["rows"]
        result = []
        for row in rows:
            result.append(row["value"])
        return result

    @staticmethod
    def FindUserByUsername(username):
        json = HttpApi.GetDB('_design/find/_view/user_by_username?key="' + username + '"')
        return Requests.ExtractRows(json)

    @staticmethod
    def DownloadDocument(documentId):
        return HttpApi.GetDB(documentId)

    @staticmethod
    def DeleteDocument(documentId):
        content = Requests.DownloadDocument(documentId)
        newContent = '{"_id":"' + content["_id"] + '", "_rev":"' + content["_rev"] + '","_deleted":true}'
        HttpApi.PostDB('', newContent)

    @staticmethod
    def UploadDocument(jsonContent):
        HttpApi.PostDB('', jsonContent)

    @staticmethod
    def FindAllUsers():
        json = HttpApi.GetDB('_design/find/_view/user_by_username')
        return Requests.ExtractRows(json)

    @staticmethod
    def FindPostsByUsername(username):
        parsed = HttpApi.GetDB('_design/find/_view/post_by_username_date?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        return Requests.ExtractRows(parsed)

    @staticmethod
    def FindRelationshipsByUsername(username):
        json_confirmed = HttpApi.GetDB('_design/find/_view/relationship_confirmed_by_username?key="' + username + '"')
        relationships_confirmed = Requests.ExtractRows(json_confirmed)

        json_proposed = HttpApi.GetDB('_design/find/_view/relationship_proposed_by_username?key="' + username + '"')
        relationships_proposed = Requests.ExtractRows(json_proposed)

        json_pending = HttpApi.GetDB('_design/find/_view/relationship_pending_by_username?key="' + username + '"')
        relationships_pending  = Requests.ExtractRows(json_pending)

        return (relationships_confirmed, relationships_proposed, relationships_pending)

    @staticmethod
    def GenerateUUID():
        json = HttpApi.Get(Config.couchUrl + '_uuids')
        uuids = json["uuids"]
        return uuids[0]

    @staticmethod
    def FindUsersByFnameSnameBday(firstName, secondName, dateOfBirth):
        if secondName and dateOfBirth:
            json = HttpApi.GetDB('_design/find/_view/user_by_fname_sname_bday'
                           '?key=["' + firstName + '","' + secondName + '","' + dateOfBirth + '"]')
        elif secondName:
            json = HttpApi.GetDB('_design/find/_view/user_by_fname_sname_bday'
                               '?startkey=["' + firstName + '","' + secondName + '"]&endkey=["' + firstName + '","' + secondName + '",{}]')
        else:
            json = HttpApi.GetDB('_design/find/_view/user_by_fname_sname_bday'
                               '?startkey=["' + firstName + '"]&endkey=["' + firstName + '",{},{}]')

        return Requests.ExtractRows(json)

    @staticmethod
    def FindUsersBySnameBday(secondName, dateOfBirth):
        if dateOfBirth:
            json = HttpApi.GetDB('_design/find/_view/user_by_sname_bday'
                               '?key=["' + secondName + '","' + dateOfBirth + '"]')
        else:
            json = HttpApi.GetDB('_design/find/_view/user_by_sname_bday'
                               '?startkey=["' + secondName + '"]&endkey=["' + secondName + '",{}]')

        return Requests.ExtractRows(json)

    @staticmethod
    def FindUsersByBdayFname(dateOfBirth, firstName):
        if firstName:
            json = HttpApi.GetDB('_design/find/_view/user_by_bday_fname'
                               '?key=["' + dateOfBirth + '","' + firstName + '"]')
        else:
            json = HttpApi.GetDB('_design/find/_view/user_by_bday_fname'
                               '?startkey=["' + dateOfBirth + '"]&endkey=["' + dateOfBirth + '",{}]')

        return Requests.ExtractRows(json)