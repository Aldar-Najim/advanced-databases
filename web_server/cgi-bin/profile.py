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

        parsed = Requests.FindHashByUsername(username)
        if len(parsed) > 0:
            hash_actual = parsed[0]["password_hash"]
            hash_specified = hashlib.md5(password.encode('utf-8')).hexdigest()
            return (hash_actual == hash_specified, True, parsed[0])
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
        (accepted, exists, user) = PageProfile.CheckHash(username, password)

        posts = None

        if not exists:
            Output.Profile("not_exists", username, password, user, posts, None, None, None)
        elif accepted:

            if page == "MYPAGE":
                posts = Requests.FindPostsByUsername(user["username"])
                Output.Profile("mypage", username, password, user, posts, None, None, None)
            elif page == "MYFRIENDS":
                (relationships_confirmed, relationships_proposed, relationships_pending) = Requests.FindRelationshipsByUsername(username)
                Output.Profile("myfriends", username, password, user, None, relationships_confirmed, relationships_proposed, relationships_pending)
            elif page == "MYGROUPS":
                Output.Profile("mygroups", username, password, user, None, None, None, None)
        else:
            Output.Profile("password_incorrect", username, password, user, posts, None, None, None)



PageProfile.Execute()