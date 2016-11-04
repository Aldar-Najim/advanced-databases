import base64

from collections import OrderedDict

from config import Config

# this class is responsible for generating html code for web-clients

class Output:

    # Prints -------------------------------------

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
    def PrintHeader(fileTo, buttonName, tab, urlTabs):
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
                Output.PrintImage('myprofile_line.png', urlTabs[0])
            else:
                Output.PrintImage('myprofile_noline.png', urlTabs[0])
            print("""
                            </td>
                            <td width="10%">
                """)
            if tab == 2:
                Output.PrintImage('myfriends_line.png', urlTabs[1])
            else:
                Output.PrintImage('myfriends_noline.png', urlTabs[1])
            print("""
                            </td>
                            <td width="10%">""")
            if tab == 3:
                Output.PrintImage('mygroups_line.png', urlTabs[2])
            else:
                Output.PrintImage('mygroups_noline.png', urlTabs[2])
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
    def PrintProfile(user, posts, users):
        print("""
            <table class="table_colored">
                <tr><h2>Profile</h2></tr>
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
            </table><br><br>""")
        for post in posts:
            print("""
                <table class="table_colored">
                    <tr><h2>Post</h2></tr>
                    <tr>
                        <td><h2>""" + post["date"] + """</h2></td>
                        <td><h2>""" + post["text"] + """</h2></td>
                        <td>""")
            Output.PrintImage('trash.png', '')
            print('</td></tr>')

            comments_ordered = OrderedDict(sorted(post["comments"].items(), key=lambda t: t[1]["date"])) # sorting by date

            for comment_id, comment in comments_ordered.items():

                foo = users[comment["username"]]["first_name"] + " " + users[comment["username"]]["second_name"]
                print("""
                    <tr>
                        <td>""" + foo + """</td>
                        <td>""" + comment["text"] + """</td>
                    </tr>""")

            print('''
            <tr>
                <td></td>
                <td>
                    <form action="/cgi-bin/profile.py">
                        <input type="text" name="COMMENT">
                        <input type="submit" class="big_button" value="Add comment">
                    </form>
                </td>
            </tr>
            ''')
            print('</table><br><br>')

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
    def PrintUserSearchForm(username, password):
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

    @staticmethod
    def PrintUserList(username, password, foundUsers):
        print('<table class="table_colored">')
        for i in range(0, len(foundUsers)):
            print('''
                <tr>
                    <td>
                        <a href="''' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                            '&WATCHUSERNAME=' + foundUsers[i]["username"] + '&PAGE=WATCH">' + foundUsers[i]["first_name"] + ' ' + foundUsers[i]["second_name"] + '</a>')
            if foundUsers[i]["relation"] == "-":
                print("""
                    <td></td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type="submit" class="big_button" value="Add">
                        </form>
                    </td>
                """)
            elif foundUsers[i]["relation"] == "proposed":
                print("""
                    <td>added you</td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type="submit" class="big_button" value="Confirm">
                        </form>
                    </td>
                    """)
            elif foundUsers[i]["relation"] == "pending":
                print("""<td>is pending</td>
                        <td>
                            <form action="/cgi-bin/profile.py">
                                <input type="submit" class="big_button" value="Reject">
                            </form>
                        </td>""")
            elif foundUsers[i]["relation"] == "confirmed":
                print("""
                    <td>you are friends</td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type="submit" class="big_button" value="Remove">
                        </form>
                    </td>
                    """)
            else:
                print('<td>is you</td><td></td>')

            print("""
                </tr>
                <tr>
                    <td height="30"></td>
                    <td height="30"></td>
                </tr>
            """)
        print('</table>')

    # Auxiliary ----------------------------------------

    @staticmethod
    def GetTabUrls(username, password):
        urlUserPassword = Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password
        urlProfile = urlUserPassword + '&PAGE=MYPAGE'
        urlFriends = urlUserPassword + '&PAGE=MYFRIENDS'
        urlGroups = urlUserPassword + '&PAGE=MYGROUPS'
        return (urlProfile, urlFriends, urlGroups)

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
    def Profile(status, username, password, user, posts, users, relationships, foundUsers):
        Output.PrintHead()
        print('<body>')

        buttonFileTo = "sign_in.py"
        buttonName = "Sign out"

        tabUrls = Output.GetTabUrls(username, password)

        if (status == "not_exists") or (status == "password_incorrect"):
            Output.PrintHeader(buttonFileTo, buttonName, None, tabUrls)
        elif status == "mypage":
            Output.PrintHeader(buttonFileTo, buttonName, 1, tabUrls)
        elif status == "myfriends" or status == "search":
            Output.PrintHeader(buttonFileTo, buttonName, 2, tabUrls)
        elif status == "mygroups":
            Output.PrintHeader(buttonFileTo, buttonName, 3, tabUrls)

        print('<div class="content"><br><br>')

        if status == "not_exists":
            print("User does not exist")
        elif status == "mypage":
            Output.PrintProfile(user, posts, users)
        elif status == "myfriends":
            Output.PrintUserSearchForm(username, password)
            Output.PrintRelationships(relationships)
            print('My friends')
        elif status == "search":
            Output.PrintUserList(username, password, foundUsers)
        elif status == "watch":
            print('Other user')
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