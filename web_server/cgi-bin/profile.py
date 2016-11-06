import cgi
import hashlib
import datetime
import json

from output import Output
from requests import Requests

class PageProfile:

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
    def GetUsersByPostList(posts):
        result = {}

        if len(posts) > 0:
            result[posts[0]["username"]] = Requests.FindUserByUsername(posts[0]["username"])[0]

        for i in range(0, len(posts)):
            for comment_id, comment in posts[i]["comments"].items():
                result[comment["username"]] = Requests.FindUserByUsername(comment["username"])[0]

        return result

    def __init__(self):
        form = cgi.FieldStorage()
        self.username = form.getfirst("USERNAME", "-")
        self.password = form.getfirst("PASSWORD", "-")
        self.page = form.getfirst("PAGE", "MYPAGE")
        if self.page == "SEARCH":
            self.usernameSearched = form.getfirst("SEARCHED", None)
            self.firstName = form.getfirst("FIRSTNAME", None)
            self.secondName = form.getfirst("SECONDNAME", None)
            self.dateOfBirth = form.getfirst("DATEOFBIRTH", None)
        elif self.page == "WATCH":
            self.watchUsername = form.getfirst("WATCHUSERNAME", None)
        elif self.page == "ADDCOMMENTPROFILE":
            self.comment = form.getfirst("COMMENT", None)
            self.watchUsername = form.getfirst("WATCHUSERNAME", None)
            self.postId = form.getfirst("POSTID", None)
        elif self.page == "ADDPOSTPROFILE":
            self.content = form.getfirst("POST", None)
        elif self.page == "DELETEPOSTPROFILE":
            self.postId = form.getfirst("POSTID", None)
        elif self.page == "DELETECOMMENTPROFILE":
            self.watchUsername = form.getfirst("WATCHUSERNAME", None)
            self.postId = form.getfirst("POSTID", None)
            self.commentId = form.getfirst("COMMENTID", None)

    def CheckHash(self):
        """
            Returns:
            Flag - if the actual hash matches the specified hash
        """

        hash_actual = self.user["password_hash"]
        hash_specified = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        return hash_actual == hash_specified

    def SearchUsers(self):
        if self.usernameSearched:
            users = Requests.FindUserByUsername(self.usernameSearched)
            if len(users) > 0:
                if self.firstName and (users[0]["first_name"] != self.firstName):
                    return None
                if self.secondName and (users[0]["second_name"] != self.secondName):
                    return None
                if self.dateOfBirth and (users[0]["date_of_birth"] != self.dateOfBirth):
                    return None
                return users
            else:
                return None
        else:
            if self.firstName and self.secondName and self.dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(self.firstName, self.secondName, self.dateOfBirth)
            elif self.firstName and self.secondName and not self.dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(self.firstName, self.secondName, self.dateOfBirth)
            elif self.firstName and not self.secondName and not self.dateOfBirth:
                return Requests.FindUsersByFnameSnameBday(self.firstName, self.secondName, self.dateOfBirth)
            elif not self.firstName and self.secondName and self.dateOfBirth:
                return Requests.FindUsersBySnameBday(self.secondName, self.dateOfBirth)
            elif not self.firstName and self.secondName and not self.dateOfBirth:
                return Requests.FindUsersBySnameBday(self.secondName, self.dateOfBirth)
            elif self.firstName and not self.secondName and self.dateOfBirth:
                return Requests.FindUsersByBdayFname(self.dateOfBirth, self.firstName)
            elif not self.firstName and not self.secondName and not self.dateOfBirth:
                return Requests.FindAllUsers()
            else:
                return Requests.FindUsersByBdayFname(self.dateOfBirth, self.firstName)

    def TagUsersByRelations(self, users, relationships):
        for i in range(0, len(users)):
            found = False

            if self.username == users[i]["username"]:
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

    def AddPostProfile(self, content):
        document = {}
        document["type"] = "post"
        document["username"] = self.username
        document["id_group"] = "-"
        document["date"] = PageProfile.GetCurrentDate()
        document["text"] = content
        document["comments"] = {}
        jsonDoc = json.dumps(document, separators=(',', ':'))
        Requests.UploadDocument(jsonDoc)

    def AddCommentPost(self):
        postContent = Requests.DownloadDocument(self.postId)
        newComment = {"username":self.username,"text":self.comment,"date":PageProfile.GetCurrentDate()}
        uuid = Requests.GenerateUUID()
        postContent["comments"][uuid] = newComment
        jsonDoc = json.dumps(postContent, separators=(',', ':'))
        Requests.UploadDocument(jsonDoc)

    def DeletePostProfile(self):
        post = Requests.DownloadDocument(self.postId)
        if (self.username == post["username"]):
            Requests.DeleteDocument(self.postId)

    def DeleteCommentProfile(self):
        post = Requests.DownloadDocument(self.postId)
        if (post["comments"][self.commentId]["username"] == self.username):
            del post["comments"][self.commentId]
            jsonPost = json.dumps(post, separators=(',', ':'))
            Requests.UploadDocument(jsonPost)

    def Execute(self):
        self.user = Requests.FindUserByUsername(self.username)
        if len(self.user) > 0:
            exists = True
            self.user = self.user[0]
            accepted = self.CheckHash()
        else:
            exists = False

        posts = None

        if not exists:
            Output.Profile("not_exists", self.username, self.password, self.user, None, posts, None, None, None)
        elif accepted:
            if self.page == "MYPAGE":
                posts = Requests.FindPostsByUsername(self.user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", self.username, self.password, self.user, posts, users, None, None, None)
            elif self.page == "MYFRIENDS":
                relationships = Requests.FindRelationshipsByUsername(self.username)
                confirmed = PageProfile.GetUsersByRelations(relationships[0])
                proposed = PageProfile.GetUsersByRelations(relationships[1])
                pending = PageProfile.GetUsersByRelations(relationships[2])
                users = {**confirmed, **proposed, **pending}
                Output.Profile("myfriends", self.username, self.password, self.user, None, users, relationships, None, None)
            elif self.page == "SEARCH":
                relationships = Requests.FindRelationshipsByUsername(self.username)
                users = self.SearchUsers()
                self.TagUsersByRelations(users, relationships)
                Output.Profile("search", self.username, self.password, self.user, None, None, relationships, users, None)
            elif self.page == "WATCH":
                watchUser = Requests.FindUserByUsername(self.watchUsername)
                if (len(watchUser) > 0):
                    watchUser = watchUser[0]
                    posts = Requests.FindPostsByUsername(watchUser["username"])
                    users = PageProfile.GetUsersByPostList(posts)
                    Output.Profile("watch", self.username, self.password, watchUser, posts, users, None, None, None)
                else:
                    Output.Profile("watch", self.username, self.password, self.user, posts, None, None, None, None)
            elif self.page == "MYGROUPS":
                Output.Profile("mygroups", self.username, self.password, self.user, None, None, None, None, None)
            elif self.page == "ADDCOMMENTPROFILE":
                watchUser = Requests.FindUserByUsername(self.watchUsername)
                if (len(watchUser) > 0):
                    watchUser = watchUser[0]
                    self.AddCommentPost()
                    posts = Requests.FindPostsByUsername(self.watchUsername)
                    users = PageProfile.GetUsersByPostList(posts)
                    if self.watchUsername == self.username:
                        Output.Profile("mypage", self.username, self.password, self.user, posts, users, None, None, None)
                    else:
                        Output.Profile("watch", self.username, self.password, watchUser, posts, users, None, None, None)
            elif self.page == "ADDPOSTPROFILE":
                self.AddPostProfile(self.content)
                posts = Requests.FindPostsByUsername(self.user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", self.username, self.password, self.user, posts, users, None, None, None)
            elif self.page == "DELETECOMMENTPROFILE":
                watchUser = Requests.FindUserByUsername(self.watchUsername)
                if (len(watchUser) > 0):
                    watchUser = watchUser[0]
                    self.DeleteCommentProfile()
                    posts = Requests.FindPostsByUsername(self.watchUsername)
                    users = PageProfile.GetUsersByPostList(posts)
                    if self.watchUsername == self.username:
                        Output.Profile("mypage", self.username, self.password, self.user, posts, users, None, None, None)
                    else:
                        Output.Profile("watch", self.username, self.password, watchUser, posts, users, None, None, None)
            elif self.page == "DELETEPOSTPROFILE":
                self.DeletePostProfile()
                posts = Requests.FindPostsByUsername(self.user["username"])
                users = PageProfile.GetUsersByPostList(posts)
                Output.Profile("mypage", self.username, self.password, self.user, posts, users, None, None, None)
        else:
            Output.Profile("password_incorrect", self.username, self.password, self.user, posts, None, None, None, None)


page = PageProfile()
page.Execute()