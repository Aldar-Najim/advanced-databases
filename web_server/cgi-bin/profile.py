import cgi
import hashlib

from output import Output
from requests import Requests

class PageProfile:

    @staticmethod
    def CheckHash(username, password):
        parsed = Requests.HashByUsername(username)
        if len(parsed["rows"]) > 0:
            id = parsed["rows"][0]["id"]
            hash_actual = parsed["rows"][0]["value"]
            hash_proposed = hashlib.md5(password.encode('utf-8')).hexdigest()
            return (hash_actual == hash_proposed, True, id)
        else:
            return (False, False, None)


    @staticmethod
    def Execute():
        form = cgi.FieldStorage()
        username = form.getfirst("USERNAME", "-")
        password = form.getfirst("PASSWORD", "-")
        page = form.getfirst("PAGE", "MYPAGE")

        posts = []
        user = None

        (accepted, exists, userId) = PageProfile.CheckHash(username, password)

        if not exists:
            Output.Profile("not_exists", username, password, user, posts)
        elif accepted:
            user = Requests.GetDocument(userId)

            if page == "MYPAGE":
                posts = Requests.FindPostIdByUsername(user["username"])
                Output.Profile("mypage", username, password, user, posts)
            elif page == "MYFRIENDS":
                Output.Profile("myfriends", username, password, user, None)
            elif page == "MYGROUPS":
                Output.Profile("mygroups", username, password, user, None)
        else:
            Output.Profile("password_incorrect", username, password, user, posts)



PageProfile.Execute()