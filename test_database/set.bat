cls

:: Reset database -------------------------------------------------------------------------------------------------

curl -X DELETE http://127.0.0.1:5984/social
curl -X PUT http://127.0.0.1:5984/social

:: Design documents ----------------------------------------------------------------------------------------------------

curl -X PUT http://localhost:5984/social/_design/find -d @find.txt
curl -X PUT http://localhost:5984/social/_design/statistics -d @statistics.txt

:: Users of the social network ---------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27014134 -d @user_1.txt
curl -X PUT http://127.0.0.1:5984/social/cff457c34484830b569a999a27016314 -d @user_2.txt
curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce37300242f -d @user_3.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd001a08 -d @user_4.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd009755 -d @user_5.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd00ce84 -d @user_6.txt
curl -X PUT http://127.0.0.1:5984/social/c30e533236a885f29a115551eb026aa3 -d @user_7.txt

:: Posts of users -----------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce3730121b0 -d @post_1_1.txt
curl -X PUT http://127.0.0.1:5984/social/a8af1fde90e8f71681da7ce373015a56 -d @post_1_2.txt
curl -X PUT http://127.0.0.1:5984/social/c30e533236a885f29a115551eb0164cf -d @post_4_1.txt
curl -X PUT http://127.0.0.1:5984/social/c30e533236a885f29a115551eb023afa -d @post_7_1.txt

:: Posts in groups -----------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/dc3399efe88b8c4c9636eaf4e101529f -d @post_1_group_1.txt

:: Relationships -------------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd00219b -d @relationship_1.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd003817 -d @relationship_2.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd0068ea -d @relationship_3.txt
curl -X PUT http://127.0.0.1:5984/social/04405f0ba7ed1e8806a1df27dd00a63d -d @relationship_4.txt
curl -X PUT http://127.0.0.1:5984/social/c30e533236a885f29a115551eb023ad3 -d @relationship_5.txt

:: Groups -------------------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64000b14 -d @group_1.txt
curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64001ab4 -d @group_2.txt
curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64004ec1 -d @group_3.txt

:: Group participations ------------------------------------------------------------------------------------------

curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64002435 -d @participation_1.txt
curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64003449 -d @participation_2.txt
curl -X PUT http://127.0.0.1:5984/social/192f2278f1902ed67c4a3f7d64003908 -d @participation_3.txt

