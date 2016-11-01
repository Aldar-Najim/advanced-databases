import cgi
import hashlib

from output import Output
from requests import Requests


class PageSignUp:

    @staticmethod
    def CreateUserJson(username, first_name, second_name, password, date_of_birth):
        return '{"type":"user", "username":"' + username + \
                           '", "first_name":"' + first_name + \
                           '", "second_name":"' + second_name + \
                           '", "password_hash":"' + hashlib.md5(password.encode('utf-8')).hexdigest() + \
                           '", "date_of_birth":"' + date_of_birth + \
                           '", "description":""}'

    @staticmethod
    def GetArguments():
        form = cgi.FieldStorage()
        username = form.getfirst("USERNAME", None)
        password = form.getfirst("PASSWORD", None)
        first_name = form.getfirst("FIRST_NAME", None)
        second_name = form.getfirst("SECOND_NAME", None)
        date_of_birth = form.getfirst("DATE_OF_BIRTH", None)
        return (username, password, first_name, second_name, date_of_birth)

    @staticmethod
    def Execute():
        (username, password, first_name, second_name, date_of_birth) = PageSignUp.GetArguments()

        if (not username) and (not password) and (not first_name) and (not second_name) and (not date_of_birth):
            Output.SignUp("not_filled")
        else:
            if username and password and first_name and second_name and date_of_birth:
                jsonHashes = Requests.FindHashByUsername(username)

                if len(jsonHashes["rows"]) > 0:
                    Output.SignUp("filled_already_exists")
                else:
                    jsonContent = PageSignUp.CreateUserJson(username, first_name, second_name, password, date_of_birth)
                    Requests.UploadDocument(jsonContent)
                    Output.SignUp("filled_created")
            else:
                Output.SignUp("filled_not_all")




PageSignUp.Execute()