import cgi
import urllib.request
import hashlib
import json
from config import config
from output import Output

# checks login and password in database, return matching flag and user id
def CheckHash(login, password):
    url = config.couch_url + '/_design/find/_view/user_by_username?key="' + login + '"'
    response = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(response)
    id = parsed["rows"][0]["id"]
    hash_actual = parsed["rows"][0]["value"]
    hash_proposed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return (hash_actual == hash_proposed, id)

def GetDocument(DocId):
    url = config.couch_url + '/' + DocId
    response = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(response)
    return parsed

def FindPostIdByUsername(username):
    url = config.couch_url + '/_design/find/_view/post_by_username?key="' + username + '"'
    response = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(response)
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
    post_ids = FindPostIdByUsername(user["username"])
    posts = []
    for id in post_ids:
        posts.append(GetDocument(id))
    Output.Profile(True, user, posts)
else:
    Output.Profile(False, None, None)


