import cgi
import urllib.request
import hashlib
import json
from config import config

def CheckHash(login, password):
    url = config.server_url + '/_design/find/_view/user?key="' + login + '"'
    response = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(response)
    id = parsed["rows"][0]["id"]
    hash_actual = parsed["rows"][0]["value"]
    hash_proposed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return (hash_actual == hash_proposed, id)

def FindUser(userId):
    url = config.server_url + '/' + userId
    response = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(response)
    return parsed

def Output(accepted, user):
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
        </table>""")
    else:
        print("Invalid credentials")
    print("</body></html>")

###################################################

form = cgi.FieldStorage()
login = form.getfirst("USERNAME", "-")
password = form.getfirst("PASSWORD", "-")

(accepted, userId) = CheckHash(login, password)
if (accepted):
    user = FindUser(userId)
    Output(True, user)
else:
    Output(False, None)


