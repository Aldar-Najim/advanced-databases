import cgi
import hashlib

from output import Output
from requests import Requests

class PageProfile:

    @staticmethod
    def CheckHash(username, password):
        """
            Takes username and password
            Returns:
            1) Flag: the actual hash matches the specified hash
            2) Flag: such user exists
            3) User data
        """

        users = Requests.FindUserByUsername(username)
        if len(users) > 0:
            hash_actual = users[0]["password_hash"]
            hash_specified = hashlib.md5(password.encode('utf-8')).hexdigest()
            return (hash_actual == hash_specified, True, users[0])
        else:
            return (False, False, None)

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
    def tagUsersByRelations(users, relationships, myUsername):
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
    def Execute():
        (username, password, page) = PageProfile.GetArguments()
        (accepted, exists, user) = PageProfile.CheckHash(username, password)

        posts = None

        if not exists:
            Output.Profile("not_exists", username, password, user, posts, None, None)
        elif accepted:

            if page == "MYPAGE":
                posts = Requests.FindPostsByUsername(user["username"])
                Output.Profile("mypage", username, password, user, posts, None, None)
            elif page == "MYFRIENDS":
                relationships = Requests.FindRelationshipsByUsername(username)
                Output.Profile("myfriends", username, password, user, None, relationships, None)
            elif page == "SEARCH":
                relationships = Requests.FindRelationshipsByUsername(username)
                searchData = PageProfile.GetSearchArguments()
                users = PageProfile.SearchUsers(searchData)
                PageProfile.tagUsersByRelations(users, relationships, username)
                Output.Profile("search", username, password, user, None, relationships, users)
            elif page == "MYGROUPS":
                Output.Profile("mygroups", username, password, user, None, None, None)

        else:
            Output.Profile("password_incorrect", username, password, user, posts, None, None)



PageProfile.Execute()