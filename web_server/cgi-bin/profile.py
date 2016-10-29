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

        posts = []
        user = None

        (accepted, exists, userId) = PageProfile.CheckHash(username, password)

        if accepted:
            user = Requests.GetDocument(userId)
            post_ids = Requests.FindPostIdByUsername(user["username"])
            for id in post_ids:
                posts.append(Requests.GetDocument(id))

        Output.Profile(accepted, exists, user, posts)



PageProfile.Execute()