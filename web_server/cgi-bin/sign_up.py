import cgi
import hashlib

from output import Output
from requests import Requests

class PageSignUp:

    def CreateUserJson(self):
        return '{"type":"user", "username":"' + self.username + \
                           '", "first_name":"' + self.firstName + \
                           '", "second_name":"' + self.secondName + \
                           '", "password_hash":"' + hashlib.md5(self.password.encode('utf-8')).hexdigest() + \
                           '", "date_of_birth":"' + self.dateOfBirth + \
                           '", "description":""}'

    def __init__(self):
        form = cgi.FieldStorage()
        self.username = form.getfirst("USERNAME", None)
        self.password = form.getfirst("PASSWORD", None)
        self.firstName = form.getfirst("FIRST_NAME", None)
        self.secondName = form.getfirst("SECOND_NAME", None)
        self.dateOfBirth = form.getfirst("DATE_OF_BIRTH", None)

    def Execute(self):
        if (not self.username) and (not self.password) and (not self.firstName) and (not self.secondName) and (not self.dateOfBirth):
            Output.SignUp("not_filled")
        else:
            if self.username and self.password and self.firstName and self.secondName and self.dateOfBirth:
                users = Requests.FindUserByUsername(self.username)

                if len(users) > 0:
                    Output.SignUp("filled_already_exists")
                else:
                    jsonContent = self.CreateUserJson()
                    Requests.UploadDocument(jsonContent)
                    Output.SignUp("filled_created")
            else:
                Output.SignUp("filled_not_all")


page = PageSignUp()
page.Execute()