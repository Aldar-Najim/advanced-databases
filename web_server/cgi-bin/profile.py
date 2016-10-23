import cgi
import urllib.request
import hashlib
import json

form = cgi.FieldStorage()
text1 = form.getfirst("USERNAME", "-")
text2 = form.getfirst("PASSWORD", "-")

url = 'http://localhost:5984/social/_design/find/_view/user?key="' + text1 + '"'
response = urllib.request.urlopen(url).read()
#parse = json.loads(response)

hash = hashlib.md5(text2.encode('utf-8')).hexdigest()

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
<html>
<head>
    <title>Social network</title>
</head>
<body>""")

print("""<h1>Processing</h1>""")
print("<p>TEXT_1: {}</p>".format(text1))
print("<p>TEXT_2: {}</p>".format(text2))

print("""</body></html>""")


