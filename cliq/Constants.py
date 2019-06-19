#gcloud_path = "gs://zinc-advice-242819.appspot.com/";
gcloud_path = "";
bucket_name = "zinc-advice-242819.appspot.com";
thumbsize   = 128;
thumbprefix = "T_";
feedBatchCount = 4;

codebase = {
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

"uUsername" 			: "username",
"uImage" 			: "image",
"uDescription" 			: "description",
"uPostId" 			: "postId",
"uTimestamp" 			: "timestamp",
"uProfileId" 			: "profileId",
"uFollowee" 			: "followee",
"uAction" 			: "action",
"uSearchKey"			: "searchkey",

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

"OK" 				: "ok",
};

def getCode(name):
	global codebase;
	return codebase[name];

dir_image  = gcloud_path + "images/";
dir_thumbs = gcloud_path + "thumbs/";

format_date = "%Y-%m-%d";
thumbnail_format = "JPEG";
