
# this class is responsible for generating html for web-clients
# different methods correspond to different web-pages

class Output:

    @staticmethod
    def PrintHeader():
        print("Content-Type: text/html\n")
        print("""<!DOCTYPE HTML>
            <html>
            <head>
                <title>Social network</title>
            </head>""")

    @staticmethod
    def SignUp():
        Output.PrintHeader()
        print("""
        <body>
            <form action="/cgi-bin/profile.py">
                <h2>Username:</h2>
                <input type="text" name="USERNAME"><br><br>
                <h2>Password:</h2>
                <input type="text" name="PASSWORD"><br><br>
                <input type="submit" value="Sign-in"><br>
            </form>
        </body>
        </html>""")

    @staticmethod
    def Profile(accepted, user, posts):
        Output.PrintHeader()
        print("""
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
        print("""
        </body>
        </html>""")