import cgi
import hashlib

from output import Output
from httpapi import HttpApi


class PageSignUp:

    @staticmethod
    def Execute():
        form = cgi.FieldStorage()
        username = form.getfirst("USERNAME")
        password = form.getfirst("PASSWORD")
        first_name = form.getfirst("FIRST_NAME")
        second_name = form.getfirst("SECOND_NAME")
        date_of_birth = form.getfirst("DATE_OF_BIRTH")

        if (not username) and (not password) and (not first_name) and (not second_name) and (not date_of_birth):
            Output.SignUp("filling")
        else:
            if username and password and first_name and second_name and date_of_birth:
                parsed = HttpApi.Get('_design/find/_view/hash_by_username?key="' + username + '"')

                if len(parsed["rows"]) > 0:
                    Output.SignUp("filled_already_exists")
                else:
                    data = '{"type":"user", "username":"' + username + \
                           '", "first_name":"' + first_name + \
                           '", "second_name":"' + second_name + \
                           '", "password_hash":"' + hashlib.md5(password.encode('utf-8')).hexdigest() + \
                           '", "date_of_birth":"' + date_of_birth + \
                           '", "description":""}'
                    HttpApi.Post('', data)
                    Output.SignUp("filled_created")
            else:
                Output.SignUp("filled_not_all")




PageSignUp.Execute()