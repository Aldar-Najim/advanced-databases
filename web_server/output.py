import base64

from collections import OrderedDict

from config import Config

# this class is responsible for generating html code for web-clients

class Output:

    # Auxiliary -------------------------------------

    @staticmethod
    def PrintHead():
        print("Content-Type: text/html\n")
        print("""<!DOCTYPE HTML>
            <html>
               <head>
                  <meta charset="utf-8">
                  <title>Social network</title>
                  <style>
                     .header {
                         width:100%;
                         height:105px;
                         background: #46BDA8;
                     }
                     .content {
                         width:60%;
                         height:300px;
                         margin-left:auto;
                         margin-right:auto;
                     }
                    .big_button {
                        background:#6CCABA;
                        border-color:#6CCABA;
                        color:white;
                        font-size : 15px;
                        font-weight: bold;
                        border-radius: 14px
                    }
                    .signup_button{
                        float:right;
                        margin-right:20px;
                        margin-top:20px;
                        width: 8em;
                        height: 4em;
                    }
                    .table_colored{
                        background-color:#c8eae4;
                    }
                    .signin_button{
                        margin-left:40px;
                        margin-top:20px;
                        width: 6em;
                        height: 2em;
                    }
                    input[type="text"], textarea {
                        background-color : #EDECE7;
                    }
                  </style>
               </head>""")

    @staticmethod
    def PrintHeader(fileTo, buttonName, tab, urlProfile, urlFriends, urlGroups):
        if not tab:
            print("""
                    <div class="header">
                        <form action="/cgi-bin/""" + fileTo + '''">
                            <input type="submit" class="big_button signup_button" value="''' + buttonName + '''">
                        </form>
                    </div>''')
        else:
            print('''
                <div class="header">
                    <table>
                        <tr>
                            <td width="20%">
                            </td>
                            <td width="10%">
                ''')
            if tab == 1:
                Output.PrintImage('myprofile_line.png', urlProfile)
            else:
                Output.PrintImage('myprofile_noline.png', urlProfile)
            print("""
                            </td>
                            <td width="10%">
                """)
            if tab == 2:
                Output.PrintImage('myfriends_line.png', urlFriends)
            else:
                Output.PrintImage('myfriends_noline.png', urlFriends)
            print("""
                            </td>
                            <td width="10%">""")
            if tab == 3:
                Output.PrintImage('mygroups_line.png', urlGroups)
            else:
                Output.PrintImage('mygroups_noline.png', urlGroups)
            print("""
                            </td>
                            <td width="20%">
                                <form action="/cgi-bin/""" + fileTo + '''">
                                    <input type="submit" class="big_button signup_button" value="''' + buttonName + '''">
                                </form>
                            </td>
                        </tr>
                    </table>
                </div>''')

    @staticmethod
    def PrintImage(imageName, reference):
        uri = base64.b64encode(open('images/' + imageName, 'rb').read()).decode('utf-8').replace('\n', '')
        imageTag = None
        if reference:
            imageTag = '''
                <a href="''' + reference + '''">
                    <img src="data:image/png;base64,{0}">
                </a>'''.format(uri)
        else:
            imageTag = '<img src="data:image/png;base64,{0}">'.format(uri)
        print(imageTag)

    @staticmethod
    def PrintProfile(user, posts):
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

            posts_ordered = OrderedDict(sorted(post["comments"].items(), key=lambda t: t[1]["date"])) # sorting by date

            for comment_id, comment_value in posts_ordered.items():
                print("""
                    <tr>
                        <td>""" + comment_value["date"] + """</td>
                        <td>""" + comment_value["text"] + """</td>
                    </tr>""")

        print("""</table>""")

    @staticmethod
    def PrintSignUpForm():
        print("""<table>
                <form action="/cgi-bin/sign_up.py">
                    <tr>
                        <td>
                            <h3>Username</h3>
                            <input type="text" name="USERNAME"><br><br>
                        </td>
                        <td>
                            <h3>Password</h3>
                            <input type="text" name="PASSWORD"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3>First name</h3>
                            <input type="text" name="FIRST_NAME"><br><br>
                        </td>
                        <td>
                            <h3>Second name</h3>
                            <input type="text" name="SECOND_NAME"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3>Date of birth</h3>
                            <input type="date" name="DATE_OF_BIRTH"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <input type="submit" class="big_button signin_button" value="Finish">
                        </td>
                    </tr>
                 </form>
            </table>""")

    @staticmethod
    def PrintSearchUserForm(username, password):
        print('''
            <table class="table_colored">
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <tr>
                        <td>
                            <h3>Username</h3>
                            <input type="text" name="SEARCHED"><br><br>
                        </td>
                        <td>
                            <h3>First name</h3>
                            <input type="text" name="FIRST_NAME"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3>Second name</h3>
                            <input type="text" name="SECOND_NAME"><br><br>
                        </td>
                        <td>
                            <h3>Date of birth</h3>
                            <input type="date" name="DATE_OF_BIRTH"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <input type="submit" class="big_button signin_button" value="Search">
                        </td>
                    </tr>
                    <input type=hidden name=PAGE value="SEARCH">
                 </form>
            </table>
        ''')

    @staticmethod
    def PrintRelationships(relationships):
        relationships_confirmed = relationships[0]
        relationships_proposed = relationships[1]
        relationships_pending = relationships[2]
        return None

    # Pages --------------------------------------------

    @staticmethod
    def SignIn():
        Output.PrintHead()
        print('<body>')
        Output.PrintHeader("sign_up.py", "Sign up", None, None, None, None)
        print('<div class="content">')


        print('''
                 <form action="/cgi-bin/profile.py">
                    <h3>Username</h3>
                    <input type="text" name="USERNAME"><br><br>
                    <h3>Password</h3>
                    <input type="text" name="PASSWORD"><br><br>
                    <input type="submit" class="big_button signin_button" value="Sign in"><br>
                 </form>
        ''')

        print('</div></body></html>')

    @staticmethod
    def Profile(status, username, password, userJson, posts, relationships, search_data):
        Output.PrintHead()
        print('<body>')

        buttonFileTo = "sign_in.py"
        buttonName = "Sign out"

        urlUserPassword = Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password
        urlProfile = urlUserPassword + '&PAGE=MYPAGE'
        urlFriends = urlUserPassword + '&PAGE=MYFRIENDS'
        urlGroups = urlUserPassword + '&PAGE=MYGROUPS'

        if (status == "not_exists") or (status == "password_incorrect"):
            Output.PrintHeader(buttonFileTo, buttonName, None, urlProfile, urlFriends, urlGroups)
        elif status == "mypage":
            Output.PrintHeader(buttonFileTo, buttonName, 1, urlProfile, urlFriends, urlGroups)
        elif status == "myfriends":
            Output.PrintHeader(buttonFileTo, buttonName, 2, urlProfile, urlFriends, urlGroups)
        elif status == "mygroups":
            Output.PrintHeader(buttonFileTo, buttonName, 3, urlProfile, urlFriends, urlGroups)


        print('<div class="content">')

        if status == "not_exists":
            print("User does not exist")
        elif status == "mypage":
            Output.PrintProfile(userJson, posts)
        elif status == "myfriends":
            Output.PrintSearchUserForm(username, password)
            Output.PrintRelationships(relationships)
            print('My friends')
        elif status == "mygroups":
            print('My groups')
        else:
            print("Password is not correct")

        print('</div></body></html>')

    @staticmethod
    def SignUp(status):
        Output.PrintHead()
        print('<body>')
        Output.PrintHeader("sign_in.py", "Return", None, None, None, None)
        print('<div class="content">')

        if status == "filled_not_all":
            print("""<font color="red">All fields must be filled!</font>""")
            Output.PrintSignUpForm()
        elif status == "not_filled":
            Output.PrintSignUpForm()
        elif status == "filled_already_exists":
            print("""User with such username is already existing""")
        else:
            print("""User account created""")

        print('</div></body></html>')