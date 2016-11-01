from httpapi import HttpApi


# this class handles different database requests using HttpApi

class Requests:

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
        parsed = HttpApi.Get('_design/find/_view/post_by_username_date?startkey=["' + username + '"]&endkey=["' + username + '",{}]&include_docs=true')
        rows = parsed["rows"]
        result = []
        for row in rows:
            result.append(row["value"])
        return result