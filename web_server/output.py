
# this class is responsible for generating html for web-clients
# different methods correspond to different web-pages

class Output:

    @staticmethod
    def PrintHeader():
        print("Content-Type: text/html\n")
        print("""<!DOCTYPE HTML>
            <html>
               <head>
                  <meta charset="utf-8">
                  <title>Social network</title>
                  <style>
                     .header {
                         width:100%;
                         height:100px;
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
    def SignIn():
        Output.PrintHeader()
        print("""
        </head>
           <body>
              <div class="header">
                <form action="/cgi-bin/sign_up.py">
                    <input type="submit" class="big_button signup_button" value="Sign up">
                </form>
             </div>
              <div class="content">
                 <form action="/cgi-bin/profile.py">
                    <h3>Username</h3>
                    <input type="text" name="USERNAME"><br><br>
                    <h3>Password</h3>
                    <input type="text" name="PASSWORD"><br><br>
                    <input type="submit" class="big_button signin_button" value="Sign in"><br>
                 </form>
              </div>
           </body>
        </html>""")

    @staticmethod
    def Profile(accepted, exists, user, posts):
        Output.PrintHeader()
        print("""
        <body>
            <div class="header">
                <form action="/cgi-bin/sign_in.py">
                    <input type="submit" class="big_button signup_button" value="Sign out">
                </form>
            </div>
            <div class="content">""")
        if not exists:
            print("User does not exist")
        elif accepted:
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
            </div>
        </body>
    </html>""")

    @staticmethod
    def SignUp():
        Output.PrintHeader()
        print("""
        <body>
            <div class="header">
                <form action="/cgi-bin/sign_in.py">
                    <input type="submit" class="big_button signup_button" value="Return">
                </form>
            </div>
            <div class="content">
                <table>
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
                                <h3>Password</h3>
                                <input type="text" name="PASSWORD"><br><br>
                            </td>
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
                </table>
            </div>
        </body>
    </html>
        """)