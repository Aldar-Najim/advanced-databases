import cgi
import hashlib
from database import Couch
from output import Output

# checks login and password in database, return matching flag and user id
def CheckHash(login, password):
    parsed = Couch.Request('_design/find/_view/hash_by_username?key="' + login + '"')
    id = parsed["rows"][0]["id"]
    hash_actual = parsed["rows"][0]["value"]
    hash_proposed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return (hash_actual == hash_proposed, id)

def GetDocument(docId):
    return Couch.Request(docId)

def FindPostsIdByUsername(username):
    parsed = Couch.Request('_design/find/_view/post_by_username_date?startkey=["' + username + '"]&endkey=["' + username + '",{}]&include_docs=true')
    rows = parsed["rows"]
    result = []
    for row in rows:
        result.append(row["value"])
    return result

###################################################

form = cgi.FieldStorage()
login = form.getfirst("USERNAME", "-")
password = form.getfirst("PASSWORD", "-")

(accepted, userId) = CheckHash(login, password)
if (accepted):
    user = GetDocument(userId)
    post_ids = FindPostsIdByUsername(user["username"])
    posts = []
    for id in post_ids:
        posts.append(GetDocument(id))
    Output.Profile(True, user, posts)
else:
    Output.Profile(False, None, None)


