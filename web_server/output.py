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
                        width: 100%;
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
    def PrintProfile(username, password, user, posts, users):
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
        if username == user["username"]:
            print('''
                <tr><h2>Add post</h2></tr>
                <table class="table_colored">
                    <form action="/cgi-bin/profile.py">
                        <input type=hidden name=USERNAME value="''' + username + '''">
                        <input type=hidden name=PASSWORD value="''' + password + '''">
                        <tr>
                            <td>
                                <input type="text" name="POST">
                            </td>
                            <td>
                                <input type="submit" class="big_button" value="Add">
                            </td>
                        </tr>
                        <input type=hidden name=PAGE value="ADDPOSTPROFILE">
                    </form>
                </table>
            ''')
        Output.PrintProfilePostSequence(username, password, user, posts, users)

    @staticmethod
    def PrintGroup(username, password, user, posts, users, group):
        print("""
            <table class="table_colored">
                <tr><h2>Group</h2></tr>
                <tr>
                    <td>Name:</td>
                    <td>""" + group["name"] + """</td>
                </tr>
                <tr>
                    <td>Description:</td>
                    <td>""" + group["description"] + """</td>
                </tr>
            </table><br><br>""")

        print('''
            <tr><h2>Add post</h2></tr>
            <table class="table_colored">
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <tr>
                        <td>
                            <input type="text" name="POST">
                        </td>
                        <td>
                            <input type="submit" class="big_button" value="Add">
                        </td>
                    </tr>
                    <input type=hidden name=GROUP value="''' + group["_id"] + '''">
                    <input type=hidden name=PAGE value="ADDPOSTGROUP">
                </form>
            </table>
        ''')
        Output.PrintGroupPostSequence(username, password, user, posts, group, users)

    @staticmethod
    def PrintGroupPostSequence(username, password, user, posts, group, users):
        for post in reversed(posts):
            print("""
                <table class="table_colored">
                    <tr><h2>Post</h2></tr>
                    <tr>
                        <td><h2>""" + users[post["username"]]["first_name"] + " " + users[post["username"]]["second_name"] + """</h2></td>
                        <td><h2>""" + post["text"] + """</h2></td>
                        <td>""" + post["date"])

            print('</td></tr>')

            comments_ordered = OrderedDict(
                sorted(post["comments"].items(), key=lambda t: t[1]["date"]))  # sorting by date

            for comment_id, comment in comments_ordered.items():
                name = users[comment["username"]]["first_name"] + " " + users[comment["username"]]["second_name"]

                if username != comment["username"]:
                    print('''
                        <tr>
                            <td><a href="''' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                          '&WATCHUSERNAME=' + comment["username"] + '&PAGE=WATCH">' + name + """</a></td>
                            <td>""" + comment["text"] + """</td>
                            <td>""" + comment["date"] + """
                        </tr>""")
                else:
                    print('''
                        <tr>
                            <td>''' + name + """</td>
                            <td>""" + comment["text"] + """</td>
                            <td>""" + comment["date"])
                    print('</td></tr>')

            print('''
            <tr>
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <td></td>
                    <td>
                        <input type="text" name="COMMENT">
                    </td>
                    <td>
                        <input type="submit" class="big_button" value="Add comment">
                    </td>
                    <input type=hidden name=POSTID value="''' + post["_id"] + '''">
                    <input type=hidden name=GROUP value="''' + group["_id"] + '''">
                    <input type=hidden name=PAGE value="ADDCOMMENTGROUP">
                </form>
            </tr>
            ''')
            print('</table><br><br>')

    @staticmethod
    def PrintProfilePostSequence(username, password, user, posts, users):
        for post in reversed(posts):
            print("""
                <table class="table_colored">
                    <tr><h2>Post</h2></tr>
                    <tr>
                        <td><h2>""" + users[post["username"]]["first_name"] + " " + users[post["username"]]["second_name"] + """</h2></td>
                        <td><h2>""" + post["text"] + """</h2></td>
                        <td>""" + post["date"])

            if username == post["username"]:
                Output.PrintImage('trash.png', Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                                  '&POSTID=' + post["_id"] + '&PAGE=DELETEPOSTPROFILE')

            print('</td></tr>')

            comments_ordered = OrderedDict(
                sorted(post["comments"].items(), key=lambda t: t[1]["date"]))  # sorting by date

            for comment_id, comment in comments_ordered.items():
                name = users[comment["username"]]["first_name"] + " " + users[comment["username"]]["second_name"]

                if username != comment["username"]:
                    print('''
                        <tr>
                            <td><a href="''' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                          '&WATCHUSERNAME=' + comment["username"] + '&PAGE=WATCH">' + name + """</a></td>
                            <td>""" + comment["text"] + """</td>
                            <td>""" + comment["date"] + """
                        </tr>""")
                else:
                    print('''
                        <tr>
                            <td>''' + name + """</td>
                            <td>""" + comment["text"] + """</td>
                            <td>""" + comment["date"])

                    Output.PrintImage("trash.png", Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                                  '&POSTID=' + post["_id"] + '&COMMENTID=' + comment_id + '&WATCHUSERNAME=' + user["username"] +'&PAGE=DELETECOMMENTPROFILE')

                    print('</td></tr>')

            print('''
            <tr>
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <td></td>
                    <td>
                        <input type="text" name="COMMENT">
                    </td>
                    <td>
                        <input type="submit" class="big_button" value="Add comment">
                    </td>
                    <input type=hidden name=POSTID value="''' + post["_id"] + '''">
                    <input type=hidden name=WATCHUSERNAME value="''' + user["username"] + '''">
                    <input type=hidden name=PAGE value="ADDCOMMENTPROFILE">
                </form>
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
                            <input type="text" name="FIRSTNAME"><br><br>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3>Second name</h3>
                            <input type="text" name="SECONDNAME"><br><br>
                        </td>
                        <td>
                            <h3>Date of birth</h3>
                            <input type="date" name="DATEOFBIRTH"><br><br>
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
            <br><br>
        ''')

    @staticmethod
    def PrintRelationships(username, password, relationships, users):
        relationships_confirmed = relationships[0]
        relationships_proposed = relationships[1]
        relationships_pending = relationships[2]

        print('<table class="table_colored">')
        for i in range(0, len(relationships_confirmed)):
            print('<tr>')
            print('<td>')
            print('<a href="' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                            '&WATCHUSERNAME=' + relationships_confirmed[i] + '&PAGE=WATCH">' +
                            users[relationships_confirmed[i]]["first_name"] + ' ' + users[relationships_confirmed[i]]["second_name"] + '</a></td>')
            print('<td>you are friends</td>')
            print('''
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type=hidden name=USERNAME value="''' + username + '''">
                            <input type=hidden name=PASSWORD value="''' + password + '''">
                            <input type="submit" class="big_button" value="Remove">
                            <input type=hidden name=OTHERUSERNAME value="''' + relationships_confirmed[i] + '''">
                            <input type=hidden name=PAGE value="REMOVEFRIEND">
                        </form>
                    </td>
                </tr>
            ''')

        for i in range(0, len(relationships_proposed)):
            print('<tr>')
            print('<td>')
            print('<a href="' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                  '&WATCHUSERNAME=' + relationships_proposed[i] + '&PAGE=WATCH">' +
                  users[relationships_proposed[i]]["first_name"] + ' ' + users[relationships_proposed[i]]["second_name"] + '</a></td>')
            print('<td>added you</td>')
            print('''
                        <td>
                            <form action="/cgi-bin/profile.py">
                                <input type=hidden name=USERNAME value="''' + username + '''">
                                <input type=hidden name=PASSWORD value="''' + password + '''">
                                <input type="submit" class="big_button" value="Confirm">
                                <input type=hidden name=OTHERUSERNAME value="''' + relationships_proposed[i] + '''">
                                <input type=hidden name=PAGE value="CONFIRMFRIEND">
                            </form>
                        </td>
                    </tr>
                ''')

        for i in range(0, len(relationships_pending)):
            print('<tr>')
            print('<td>')
            print('<a href="' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                  '&WATCHUSERNAME=' + relationships_pending[i] + '&PAGE=WATCH">' +
                  users[relationships_pending[i]]["first_name"] + ' ' + users[relationships_pending[i]]["second_name"] + '</a></td>')
            print('<td>is pending</td>')
            print('''
                            <td>
                                <form action="/cgi-bin/profile.py">
                                    <input type=hidden name=USERNAME value="''' + username + '''">
                                    <input type=hidden name=PASSWORD value="''' + password + '''">
                                    <input type="submit" class="big_button" value="Reject">
                                    <input type=hidden name=OTHERUSERNAME value="''' + relationships_pending[i] + '''">
                                    <input type=hidden name=PAGE value="REJECTFRIEND">
                                </form>
                            </td>
                        </tr>
                    ''')
        print('</table>')

    @staticmethod
    def PrintUserSearchResults(username, password, foundUsers):
        print('<table class="table_colored">')
        for i in range(0, len(foundUsers)):
            print('''
                <tr>
                    <td>
                        <a href="''' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                            '&WATCHUSERNAME=' + foundUsers[i]["username"] + '&PAGE=WATCH">' +
                            foundUsers[i]["first_name"] + ' ' + foundUsers[i]["second_name"] + '</a></td>')
            if foundUsers[i]["relation"] == "-":
                print('''
                    <td></td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type=hidden name=USERNAME value="''' + username + '''">
                            <input type=hidden name=PASSWORD value="''' + password + '''">
                            <input type="submit" class="big_button" value="Add">
                            <input type=hidden name=OTHERUSERNAME value="''' + foundUsers[i]["username"] + '''">
                            <input type=hidden name=PAGE value="ADDFRIEND">
                        </form>
                    </td>
                ''')
            elif foundUsers[i]["relation"] == "proposed":
                print('''
                    <td>added you</td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type=hidden name=USERNAME value="''' + username + '''">
                            <input type=hidden name=PASSWORD value="''' + password + '''">
                            <input type="submit" class="big_button" value="Confirm">
                            <input type=hidden name=OTHERUSERNAME value="''' + foundUsers[i]["username"] + '''">
                            <input type=hidden name=PAGE value="CONFIRMFRIEND">
                        </form>
                    </td>
                    ''')
            elif foundUsers[i]["relation"] == "pending":
                print('''<td>is pending</td>
                        <td>
                            <form action="/cgi-bin/profile.py">
                                <input type=hidden name=USERNAME value="''' + username + '''">
                                <input type=hidden name=PASSWORD value="''' + password + '''">
                                <input type="submit" class="big_button" value="Reject">
                                <input type=hidden name=OTHERUSERNAME value="''' + foundUsers[i]["username"] + '''">
                                <input type=hidden name=PAGE value="REJECTFRIEND">
                            </form>
                        </td>''')
            elif foundUsers[i]["relation"] == "confirmed":
                print('''
                    <td>you are friends</td>
                    <td>
                        <form action="/cgi-bin/profile.py">
                            <input type=hidden name=USERNAME value="''' + username + '''">
                            <input type=hidden name=PASSWORD value="''' + password + '''">
                            <input type="submit" class="big_button" value="Remove">
                            <input type=hidden name=OTHERUSERNAME value="''' + foundUsers[i]["username"] + '''">
                            <input type=hidden name=PAGE value="REMOVEFRIEND">
                        </form>
                    </td>
                    ''')
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

    @staticmethod
    def PrintGroupSearchResults(username, password, groups):
        print('<table class="table_colored">')
        for group in groups:
            print('''
               <tr>
                    <td>
                        <a href="''' + Config.webUrl + 'profile.py?USERNAME=' + username + '&PASSWORD=' + password +
                            '&GROUP=' + group["_id"] + '&PAGE=WATCHGROUP">' + group["name"] + '</a>' +
                    '''</td>
                    <td>''')
            if group["joined"]:
                print('''
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <input type="submit" class="big_button" value="Unjoin">
                    <input type=hidden name=GROUP value="''' + group['_id'] + '''">
                    <input type=hidden name=PAGE value="UNJOIN">
                </form>
            ''')
            else:
                print('''
                <form action="/cgi-bin/profile.py">
                    <input type=hidden name=USERNAME value="''' + username + '''">
                    <input type=hidden name=PASSWORD value="''' + password + '''">
                    <input type="submit" class="big_button" value="Join">
                    <input type=hidden name=GROUP value="''' + group['_id'] + '''">
                    <input type=hidden name=PAGE value="JOIN">
                </form>
            ''')
        print('''
                    </td>
                </tr>
            ''')
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
        Output.PrintHeader("sign_up.py", "Sign up", None, None)
        print('<div class="content">')


        print('''
                 <form action="/cgi-bin/profile.py">
                    <h3>Username</h3>
                    <input type="text" name="USERNAME"><br><br>
                    <h3>Password</h3>
                    <input type="text" name="PASSWORD"><br><br>
                    <input type="submit" class="big_button signin_button" value="Sign in"><br>
                    <input type=hidden name=PAGE value="MYPAGE">
                 </form>
        ''')

        print('</div></body></html>')

    @staticmethod
    def Profile(status, username, password, user, posts, users, relationships, foundUsers, foundGroups):
        Output.PrintHead()
        print('<body>')

        buttonFileTo = "sign_in.py"
        buttonName = "Sign out"

        tabUrls = Output.GetTabUrls(username, password)

        if (status == "not_exists") or (status == "password_incorrect"):
            Output.PrintHeader(buttonFileTo, buttonName, None, tabUrls)
        elif status == "mypage":
            Output.PrintHeader(buttonFileTo, buttonName, 1, tabUrls)
        elif status == "myfriends" or status == "search" or status == "watch" \
                or status == "addfriend" or status == "confirmfriend" or status == "removefriend" or status == "rejectfriend":
            Output.PrintHeader(buttonFileTo, buttonName, 2, tabUrls)
        elif status == "mygroups" or status == "group":
            Output.PrintHeader(buttonFileTo, buttonName, 3, tabUrls)

        print('<div class="content"><br><br>')

        if status == "not_exists":
            print("User does not exist")
        elif status == "mypage":
            Output.PrintProfile(username, password, user, posts, users)
        elif status == "myfriends":
            Output.PrintUserSearchForm(username, password)
            Output.PrintRelationships(username, password, relationships, users)
        elif status == "search":
            Output.PrintUserSearchResults(username, password, foundUsers)
        elif status == "watch":
            if user:
                Output.PrintProfile(username, password, user, posts, users)
            else:
                print("Not found")
        elif status == "group":
            Output.PrintGroup(username, password, user, posts, users, foundGroups)
        elif status == "mygroups":
            Output.PrintGroupSearchResults(username, password, foundGroups)
        elif status == "addfriend":
            print('Added')
        elif status == "removefriend":
            print('Removed')
        elif status == "confirmfriend":
            print('Confirmed')
        elif status == "rejectfriend":
            print('Rejected')
        else:
            print("Password is not correct")

        print('</div></body></html>')

    @staticmethod
    def SignUp(status):
        Output.PrintHead()
        print('<body>')
        Output.PrintHeader("sign_in.py", "Return", None, None)
        print('<div class="content">')

        if status == "filled_not_all":
            print('<font color="red">All fields must be filled!</font>')
            Output.PrintSignUpForm()
        elif status == "not_filled":
            Output.PrintSignUpForm()
        elif status == "filled_already_exists":
            print('<font color="red">User with such username is already existing</font>')
            Output.PrintSignUpForm()
        else:
            print('<font color="red">User account created</font>')
            Output.PrintSignUpForm()

        print('</div></body></html>')