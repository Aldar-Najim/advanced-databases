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
            3) User id
        """

        parsed = Requests.FindHashByUsername(username)
        if len(parsed["rows"]) > 0:
            id = parsed["rows"][0]["id"]
            hash_actual = parsed["rows"][0]["value"]
            hash_specified = hashlib.md5(password.encode('utf-8')).hexdigest()
            return (hash_actual == hash_specified, True, id)
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
    def Execute():
        (username, password, page) = PageProfile.GetArguments()
        (accepted, exists, userId) = PageProfile.CheckHash(username, password)

        posts = []
        user = None

        if not exists:
            Output.Profile("not_exists", username, password, user, posts)
        elif accepted:
            user = Requests.DownloadDocument(userId)

            if page == "MYPAGE":
                posts = Requests.FindPostsByUsername(user["username"])
                Output.Profile("mypage", username, password, user, posts)
            elif page == "MYFRIENDS":
                Output.Profile("myfriends", username, password, user, None)
            elif page == "MYGROUPS":
                Output.Profile("mygroups", username, password, user, None)
        else:
            Output.Profile("password_incorrect", username, password, user, posts)



PageProfile.Execute()