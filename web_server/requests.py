import json

from httpapi import HttpApi
from config import Config


# this class handles different database requests using HttpApi

class Requests:

    @staticmethod
    def ExtractRowValues(parsed):
        rows = parsed["rows"]
        result = []
        for row in rows:
            result.append(row["value"])
        return result

    @staticmethod
    def FindUserByUsername(username):
        json = HttpApi.GetDB('_design/find/_view/user_by_username?key="' + username + '"')
        return Requests.ExtractRowValues(json)

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
        return Requests.ExtractRowValues(json)

    @staticmethod
    def FindPostsByUsername(username):
        parsed = HttpApi.GetDB('_design/find/_view/post_by_username_date?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        return Requests.ExtractRowValues(parsed)

    @staticmethod
    def ExtractSecondUsers(dictRelations):
        result = []
        for row in dictRelations["rows"]:
            result.append(row["key"][1])
        return result

    @staticmethod
    def FindRelationshipsByUsername(username):
        json_confirmed = HttpApi.GetDB('_design/find/_view/relationship_confirmed_by_username?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        relationships_confirmed = Requests.ExtractSecondUsers(json_confirmed)

        json_proposed = HttpApi.GetDB('_design/find/_view/relationship_proposed_by_username?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        relationships_proposed = Requests.ExtractSecondUsers(json_proposed)

        json_pending = HttpApi.GetDB('_design/find/_view/relationship_pending_by_username?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        relationships_pending  = Requests.ExtractSecondUsers(json_pending)

        return (relationships_confirmed, relationships_proposed, relationships_pending)

    @staticmethod
    def FindRelationshipProposed(username1, username2):
        json = HttpApi.GetDB('_design/find/_view/relationship_proposed_by_username?key=["' + username1 + '","' + username2 + '"]')
        return Requests.ExtractRowValues(json)

    @staticmethod
    def FindRelationshipConfirmed(username1, username2):
        json = HttpApi.GetDB('_design/find/_view/relationship_confirmed_by_username?key=["' + username1 + '","' + username2 + '"]')
        return Requests.ExtractRowValues(json)

    @staticmethod
    def FindRelationshipPending(username1, username2):
        json = HttpApi.GetDB('_design/find/_view/relationship_pending_by_username?key=["' + username1 + '","' + username2 + '"]')
        return Requests.ExtractRowValues(json)

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

        return Requests.ExtractRowValues(json)

    @staticmethod
    def FindUsersBySnameBday(secondName, dateOfBirth):
        if dateOfBirth:
            json = HttpApi.GetDB('_design/find/_view/user_by_sname_bday'
                               '?key=["' + secondName + '","' + dateOfBirth + '"]')
        else:
            json = HttpApi.GetDB('_design/find/_view/user_by_sname_bday'
                               '?startkey=["' + secondName + '"]&endkey=["' + secondName + '",{}]')

        return Requests.ExtractRowValues(json)

    @staticmethod
    def AddRelationship(usernameAdding, usernameAdded):
        relation = {"type":"relationship", "username1":usernameAdding, "username2":usernameAdded,"confirmed1":"yes", "confirmed2":"no"}
        relationJson = json.dumps(relation, separators=(',', ':'))
        Requests.UploadDocument(relationJson)

    @staticmethod
    def ConfirmRelationship(usernameConfirming, usernameConfirmed):
        documentId = Requests.FindRelationshipProposed(usernameConfirming, usernameConfirmed)[0]
        relation = Requests.DownloadDocument(documentId)
        if (relation["username1"] == usernameConfirming):
            relation["confirmed1"] = "yes"
        else:
            relation["confirmed2"] = "yes"
        relationJson = json.dumps(relation, separators=(',', ':'))
        Requests.UploadDocument(relationJson)

    @staticmethod
    def RemoveRelationship(usernameRemoving, usernameRemoved):
        documentId = Requests.FindRelationshipConfirmed(usernameRemoving, usernameRemoved)[0]
        relation = Requests.DownloadDocument(documentId)
        if (relation["username1"] == usernameRemoving):
            relation["confirmed1"] = "no"
        else:
            relation["confirmed2"] = "no"
        relationJson = json.dumps(relation, separators=(',', ':'))
        Requests.UploadDocument(relationJson)

    @staticmethod
    def RejectRelationship(usernameRejecting, usernameRejected):
        documentId = Requests.FindRelationshipPending(usernameRejecting, usernameRejected)[0]
        relation = Requests.DownloadDocument(documentId)
        if (relation["username1"] == usernameRejecting):
            Requests.DeleteDocument(documentId)

    @staticmethod
    def FindUsersByBdayFname(dateOfBirth, firstName):
        if firstName:
            json = HttpApi.GetDB('_design/find/_view/user_by_bday_fname'
                               '?key=["' + dateOfBirth + '","' + firstName + '"]')
        else:
            json = HttpApi.GetDB('_design/find/_view/user_by_bday_fname'
                               '?startkey=["' + dateOfBirth + '"]&endkey=["' + dateOfBirth + '",{}]')

        return Requests.ExtractRowValues(json)