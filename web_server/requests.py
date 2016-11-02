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
        return HttpApi.Get('_design/find/_view/hash_by_username?key="' + username + '"')

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
        parsed_confirmed = HttpApi.Get('_design/find/_view/relationship_confirmed_by_username?key="' + username + '"')
        relationships_confirmed = Requests.ExtractRows(parsed_confirmed)

        parsed_proposed = HttpApi.Get('_design/find/_view/relationship_proposed_by_username?key="' + username + '"')
        relationships_proposed = Requests.ExtractRows(parsed_proposed)

        parsed_pending = HttpApi.Get('_design/find/_view/relationship_pending_by_username?key="' + username + '"')
        relationships_pending  = Requests.ExtractRows(parsed_pending)

        return (relationships_confirmed, relationships_proposed, relationships_pending)
