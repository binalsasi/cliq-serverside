#gcloud_path = "gs://zinc-advice-242819.appspot.com/";
gcloud_path = "";
bucket_name = "zinc-advice-242819.appspot.com";
thumbsize   = 128;
thumbprefix = "T_";
feedBatchCount = 4;

ecode_imageExists		= "E:0x70001";
ecode_usernameAlreadyExists	= "E:0x80001";
ecode_emptyUsername 		= "E:0x80002";
ecode_noFeeds			= "E:0x80003";
ecode_noSuchUser		= "E:0x80004";
ecode_notPost 			= "E:0x90001";

uUsername	= "username";
uImage		= "image";
uDescription	= "description";
uPostId		= "postId";
uTimestamp	= "timestamp";
uProfileId	= "profileId";

dKey		= "lastkey";
dUsername	= "username";
dStatus		= "status";
dId		= "id";
dPath		= "path";
dDescription	= "description";
dB64string	= "b64string";
dPostId		= "postId";
dTimestamp	= "timestamp";
dProfileId	= "profileId";
dThumbs		= "thumblist";

str_helloWorld = "Hello World!";
str_ok = "ok";

dir_image  = gcloud_path + "images/";
dir_thumbs = gcloud_path + "thumbs/";

format_date = "%Y-%m-%d";
thumbnail_format = "JPEG";
