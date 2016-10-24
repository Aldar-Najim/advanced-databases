import cgi
import urllib.request
import hashlib
import json
from config import config

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


def Output(accepted, user, posts):
    print("Content-type: text/html\n")
    print("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <title>Social network</title>
    </head>
    <body>""")
    if (accepted):
        print("""
        <table>
            <tr>
                <td>First name:</td>
                <td>""" + user["first_name"] + """</td>
            </tr>
            <tr>
                <td>Second name:</td>
                <td>""" + user["second_name"] + """</td>
            </tr>
            <tr>
                <td>Date of birth:</td>
                <td>""" + user["date_of_birth"] + """</td>
            </tr>
            <tr>
                <td>Description:</td>
                <td>""" + user["description"] + """</td>
            </tr>""")
        for post in posts:
            print("""
            <tr>
                <td>""" + post["date"] + """</td>
                <td>""" + post["text"] + """</td>
            </tr>""")
        print("""</table>""")
    else:
        print("Invalid credentials")
    print("</body></html>")

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
    Output(True, user, posts)
else:
    Output(False, None, None)


