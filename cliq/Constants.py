#
#	Constants.py
#
#	This file contains constants, keywords, error codes etc which is used 
#	in the app.
#


# constants

gcloud_path = "";
bucket_name = "zinc-advice-242819.appspot.com";
thumbsize   = 128;
thumbprefix = "T_";
feedBatchCount = 4;
discoverPeopleCount = 10;
maxDeleteTimeinSeconds = 10 * 60;
dir_image  = gcloud_path + "images/";
dir_thumbs = gcloud_path + "thumbs/";

format_date = "%Y-%m-%d";
thumbnail_format = "JPEG";


# code base

codebase = {

# error codes
"ecode_imageExists" 		: "E:0x70001",
"ecode_usernameAlreadyExists" 	: "E:0x80001",
"ecode_emptyUsername " 		: "E:0x80002",
"ecode_noFeeds"			: "E:0x80003",
"ecode_noSuchUser" 		: "E:0x80004",
"ecode_notPost " 		: "E:0x90001",
"ecode_unableFollow" 		: "E:0x80005",
"ecode_alreadyFollow" 		: "E:0x80006",
"ecode_notFollowed" 		: "E:0x80007",
"ecode_noFollowers" 		: "E:0x80008",
"ecode_noRequests" 		: "E:0x80009",
"ecode_noSelfFollow" 		: "E:0x80010",
"ecode_badAction" 		: "E:0x80011",
"ecode_noRequest" 		: "E:0x80012",
"ecode_noResult"		: "E:0x80013",
"ecode_noFollowing"		: "E:0x80014",
"ecode_noSuchPost"		: "E:0x80015",
"ecode_alreadyLiked"		: "E:0x80016",
"ecode_notLiked"		: "E:0x80017",
"ecode_unableToLike"		: "E:0x80018",
"ecode_unableToComment"		: "E:0x80019",
"ecode_tooLate"			: "E:0x80020",
"ecode_noSuchComment"		: "E:0x80021",
"ecode_noComments"		: "E:0x80022",
"ecode_notFollowing"		: "E:0x80023",

# upstream key words
"uUsername" 			: "username",
"uImage" 			: "image",
"uDescription" 			: "description",
"uPostId" 			: "postId",
"uTimestamp" 			: "timestamp",
"uProfileId" 			: "profileId",
"uFollowee" 			: "followee",
"uAction" 			: "action",
"uSearchKey"			: "searchkey",
"uText"				: "text",
"uCommentId"			: "commentId",

# downstream key words
"dKey" 				: "lastkey",
"dUsername" 			: "username",
"dStatus" 			: "status",
"dId" 				: "id",
"dPath" 			: "path",
"dDescription" 			: "description",
"dB64string" 			: "b64string",
"dBase64String"			: "b64string",
"dPostId" 			: "postId",
"dTimestamp" 			: "timestamp",
"dProfileId" 			: "profileId",
"dThumbs" 			: "thumblist",
"dFollower" 			: "follower",
"dFollowStatus" 		: "status",
"dFollowee" 			: "followee",
"dLikes"			: "likedby",
"dCommentId"			: "commentId",
"dText"				: "dText",

# OK
"OK" 				: "ok",
};

# getCode() to get code from the code base
def getCode(name):
	global codebase;
	return codebase[name];
