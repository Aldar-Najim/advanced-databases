curl -X DELETE http://127.0.0.1:5984/social
curl -X PUT http://127.0.0.1:5984/social


:: Users of the social network ---------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27014134 -d ^
"{^
	\"type\":\"user\",^
	\"username\":\"aldar\",^
	\"first_name\":\"Aldar\",^
	\"second_name\":\"Saranov\",^
	\"password_hash\":\"827ccb0eea8a706c4c34a16891f84e7b\",^
	\"date_of_birth\":\"10.05.1995\",^
	\"description\":\"Here is description about this user\"^
}"

curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27016314 -d ^
"{^
	\"type\":\"user\",^
	\"username\":\"najim\",^
	\"first_name\":\"Najim\",^
	\"second_name\":\"Essakali\",^
	\"password_hash\":\"827ccb0eea8a706c4c34a16891f84e7b\",^
	\"date_of_birth\":\"01.01.1995\",^
	\"description\":\"Here is description about this user\"^
}"

curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce37300242f -d ^
"{^
	\"type\":\"user\",^
	\"username\":\"john \",^
	\"first_name\":\"John\",^
	\"second_name\":\"Smith\",^
	\"password_hash\":\"827ccb0eea8a706c4c34a16891f84e7b\",^
	\"date_of_birth\":\"01.01.1995\",^
	\"description\":\"Here is description about this user\"^
}"

:: Design documents ----------------------------------------------------------------------------------------------------

curl -X PUT http://localhost:5984/social/_design/find -d @find.txt