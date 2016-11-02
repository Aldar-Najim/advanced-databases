from httpapi import HttpApi


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
    def FindHashByUsername(username):
        json = HttpApi.Get('_design/find/_view/user_by_username?key="' + username + '"')
        return Requests.ExtractRows(json)

    @staticmethod
    def DownloadDocument(documentId):
        return HttpApi.Get(documentId)

    @staticmethod
    def UploadDocument(jsonContent):
        HttpApi.Post('', jsonContent)

    @staticmethod
    def FindPostsByUsername(username):
        parsed = HttpApi.Get('_design/find/_view/post_by_username_date?startkey=["' + username + '"]&endkey=["' + username + '",{}]')
        return Requests.ExtractRows(parsed)

    @staticmethod
    def FindRelationshipsByUsername(username):
        json_confirmed = HttpApi.Get('_design/find/_view/relationship_confirmed_by_username?key="' + username + '"')
        relationships_confirmed = Requests.ExtractRows(json_confirmed)

        json_proposed = HttpApi.Get('_design/find/_view/relationship_proposed_by_username?key="' + username + '"')
        relationships_proposed = Requests.ExtractRows(json_proposed)

        json_pending = HttpApi.Get('_design/find/_view/relationship_pending_by_username?key="' + username + '"')
        relationships_pending  = Requests.ExtractRows(json_pending)

        return (relationships_confirmed, relationships_proposed, relationships_pending)
