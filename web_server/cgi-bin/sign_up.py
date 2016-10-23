print("Content-Type: text/html\n")

print("""<!DOCTYPE HTML>
<html>
<head>
    <title>Social network</title>
</head>
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
