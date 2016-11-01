curl -X DELETE http://127.0.0.1:5984/social
curl -X PUT http://127.0.0.1:5984/social


:: Users of the social network ---------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27014134 -d @user_1.txt
curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27016314 -d @user_2.txt
curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce37300242f -d @user_3.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd001a08 -d @user_4.txt

:: Posts of users -----------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce3730121b0 -d @post_1_1.txt
curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce373015a56 -d @post_1_2.txt

:: Relationships -------------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd00219b -d @relationship_1.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd003817 -d @relationship_2.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd0068ea -d @relationship_3.txt

:: Design documents ----------------------------------------------------------------------------------------------------

curl -X PUT http://localhost:5984/social/_design/find -d @find.txt