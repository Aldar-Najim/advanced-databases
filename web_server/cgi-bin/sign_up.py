import cgi
from output import Output
import hashlib
from database import Couch


form = cgi.FieldStorage()
username = form.getfirst("USERNAME", "-")
password = form.getfirst("PASSWORD", "-")
first_name = form.getfirst("FIRST_NAME", "-")
second_name = form.getfirst("SECOND_NAME", "-")
date_of_birth = form.getfirst("DATE_OF_BIRTH", "-")


data = '{"type":"user", "username":"' + username + \
       '", "first_name":"' + first_name + \
       '", "second_name":"' + second_name + \
       '", "password_hash":"' + hashlib.md5(password.encode('utf-8')).hexdigest() + \
       '", "date_of_birth":"' + date_of_birth + \
       '", "description":""}'

Couch.Post('', data)

Output.SignUp()