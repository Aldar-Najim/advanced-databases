import cgi
import hashlib
import datetime
import json

from output import Output
from requests import Requests

class PageProfile:

    @staticmethod
    def CheckHash(username, password, user):
        """
            Takes username, password and found user data
            Returns:
            Flag: the actual hash matches the specified hash
        """

        hash_actual = user["password_hash"]
        hash_specified = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hash_actual == hash_specified

    @staticmethod
    def GetArguments():
        form = cgi.FieldStorage()
        username = form.getfirst("USERNAME", "-")
        password = form.getfirst("PASSWORD", "-")
        page = form.getfirst("PAGE", "MYPAGE")
        return (username, password, page)

    @staticmethod
    def GetSearchArguments():
        form = cgi.FieldStorage()
        searched = form.getfirst("SEARCHED", None)
        first_name = form.getfirst("FIRST_NAME", None)
        second_name = form.getfirst("SECOND_NAME", None)
        date_of_birth = form.getfirst("DATE_OF_BIRTH", None)
        return (searched, first_name, second_name, date_of_birth)

    @staticmethod
    def GetWatchArgument():
        form = cgi.FieldStorage()
        return form.getfirst("WATCHUSERNAME", None)

    @staticmethod
    def SearchUsers(searchData):
        username = searchData[0]
        firstName = searchData[1]
        secondName = searchData[2]
        dateOfBirth = searchData[3]

        if username:
            users = Requests.FindUserByUsername(username)
            if len(users) > 0:
                if firstName and (users[0]["first_name"] != firstName):
                    return None
                if secondName and (users[0]["second_name"] != secondName):
                    return None
                if dateOfBirth and (users[0]["date_of_birth"] != dateOfBirth):
                    return None
                return users
            else:
                return None
        else:
            if firstName and secondName and dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(firstName, secondName, dateOfBirth)
            elif firstName and secondName and not dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(firstName, secondName, dateOfBirth)
            elif firstName and not secondName and not dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(firstName, secondName, dateOfBirth)
            elif not firstName and secondName and dateOfBirth:
                return Requests.FindUsersBySnameBday(secondName, dateOfBirth)
            elif not firstName and secondName and not dateOfBirth:
                return Requests.FindUsersBySnameBday(secondName, dateOfBirth)
            elif firstName and not secondName and dateOfBirth:
                return Requests.FindUsersByBdayFname(dateOfBirth, firstName)
            elif not firstName and not secondName and not dateOfBirth:
                return Requests.FindAllUsers()
            else:
                return Requests.FindUsersByBdayFname(dateOfBirth, firstName)

    @staticmethod
    def TagUsersByRelations(users, relationships, myUsername):
        for i in range(0, len(users)):
            found = False

            if myUsername == users[i]["username"]:
                users[i]["relation"] = "me"
                found = True

            for j in range(0, len(relationships[0])):
                if users[i]["username"] == relationships[0][j][0]:
                    users[i]["relation"] = "confirmed"
                    found = True
                    break

            if not found:
                for j in range(0, len(relationships[1])):
                    if users[i]["username"] == relationships[1][j][0]:
                        users[i]["relation"] = "proposed"
                        found = True
                        break

            if not found:
                for j in range(0, len(relationships[2])):
                    if users[i]["username"] == relationships[2][j][0]:
                        users[i]["relation"] = "pending"
                        found = True
                        break

            if not found:
                users[i]["relation"] = "-"

        return users

    @staticmethod
    def GetUsersByRelations(relationships):
        result = {}

        for i in range(0, len(relationships)):
            result[relationships[i][0]] = Requests.FindUserByUsername(relationships[i][0])[0]

        return result

    @staticmethod
    def GetCurrentDate():
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def AddPostProfile(username, content):
        document = {}
        document["type"] = "post"
        document["username"] = username
        document["id_group"] = "-"
        document["date"] = PageProfile.GetCurrentDate()
        document["text"] = content
        document["comments"] = {}
        jsonDoc = json.dumps(document, separators=(',',':'))
        Requests.UploadDocument(jsonDoc)

    @staticmethod
    def GetUsersByPostList(posts):
        result = {}

        if len(posts) > 0:
            result[posts[0]["username"]] = Requests.FindUserByUsername(posts[0]["username"])[0]

        for i in range(0, len(posts)):
            for comment_id, comment in posts[i]["comments"].items():
                result[comment["username"]] = Requests.FindUserByUsername(comment["username"])[0]

        return result

    @staticmethod
    def GetCommentProfileArgument():
        form = cgi.FieldStorage()
        comment = form.getfirst("COMMENT", None)
        postId = form.getfirst("POSTID", None)
        return (comment, postId)

    @staticmethod
    def GetPostProfileArguments():
        form = cgi.FieldStorage()
        content = form.getfirst("POST", None)
        return (content)

    @staticmethod
    def AddCommentToPost(username, password, comment, postId):
        postContent = Requests.DownloadDocument(postId)
        newComment = {"username":username,"text":comment,"date":PageProfile.GetCurrentDate()}
        uuid = Requests.GenerateUUID()
        postContent["comments"][uuid] = newComment
        jsonDoc = json.dumps(postContent, separators=(',', ':'))
        Requests.UploadDocument(jsonDoc)

    @staticmethod
    def GetDeletePostArguments():
        form = cgi.FieldStorage()
        return form.getfirst("POSTID", None)

    @staticmethod
    def DeletePost(username, postId):
        post = Requests.DownloadDocument(postId)
        if (username == post["username"]):
            Requests.DeleteDocument(postId)

    @staticmethod
    def Execute():
        (username, password, page) = PageProfile.GetArguments()
        user = Requests.FindUserByUsername(username)

        if len(user) > 0:
            exists = True
            user = user[0]
            accepted = PageProfile.CheckHash(username, password, user)
        else:
            exists = False

        posts = None

        if not exists:
            Output.Profile("not_exists", username, password, user, None, posts, None, None)
        elif accepted:

            if page == "MYPAGE":
                posts = Requests.FindPostsByUsername(user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", username, password, user, posts, users, None, None)
            elif page == "MYFRIENDS":
                relationships = Requests.FindRelationshipsByUsername(username)
                confirmed = PageProfile.GetUsersByRelations(relationships[0])
                proposed = PageProfile.GetUsersByRelations(relationships[1])
                pending = PageProfile.GetUsersByRelations(relationships[2])
                users = {**confirmed, **proposed, **pending}
                Output.Profile("myfriends", username, password, user, None, users, relationships, None)
            elif page == "SEARCH":
                relationships = Requests.FindRelationshipsByUsername(username)
                searchData = PageProfile.GetSearchArguments()
                users = PageProfile.SearchUsers(searchData)
                PageProfile.TagUsersByRelations(users, relationships, username)
                Output.Profile("search", username, password, user, None, None, relationships, users)
            elif page == "WATCH":
                watchUsername = PageProfile.GetWatchArgument()
                user = Requests.FindUserByUsername(watchUsername)
                posts = Requests.FindPostsByUsername(user["username"])
                Output.Profile("watch", username, password, user, posts, None, None, None)
            elif page == "MYGROUPS":
                Output.Profile("mygroups", username, password, user, None, None, None, None)
            elif page == "COMMENTPROFILE":
                arguments = PageProfile.GetCommentProfileArgument()
                PageProfile.AddCommentToPost(username, password, arguments[0], arguments[1])
                posts = Requests.FindPostsByUsername(user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", username, password, user, posts, users, None, None)
            elif page == "POSTPROFILE":
                content = PageProfile.GetPostProfileArguments()
                PageProfile.AddPostProfile(username, content)
                posts = Requests.FindPostsByUsername(user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", username, password, user, posts, users, None, None)
            elif page == "DELETEPOST":
                postId = PageProfile.GetDeletePostArguments()
                PageProfile.DeletePost(username, postId)
                posts = Requests.FindPostsByUsername(user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", username, password, user, posts, users, None, None)


        else:
            Output.Profile("password_incorrect", username, password, user, posts, None, None, None)



PageProfile.Execute()