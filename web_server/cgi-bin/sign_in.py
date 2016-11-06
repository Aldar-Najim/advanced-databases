from output import Output

class PageSignIn:

    def Execute(self):
        Output.SignIn()


page = PageSignIn()
page.Execute()