#
#	Fetch Functions
#
#	This file contains basic functions used for fetching data.
#	This file is still a work in progress. The functionalities work,
#	more or less, But it still requires a lot of security and functional
#	checks (such as empty inputs) and so on.
#



from django.http import HttpResponse;
from django.db import IntegrityError;
from django.db.models import Q;
from cliq_backend.models import User, Images, Follows, Likes, Comments;
from datetime import datetime;
import Constants;
import random;
import base64;
import json;
import Functions;


# fetch_home() is used to fetch data for the user home page.
# this includes the post image thumbnail, post id, liked users, etc..
def fetch_home(request):
	if request.method == "POST":

		username = request.POST.get(Constants.getCode("uUsername"), '');

		images = Images.objects.filter(owner = username);

		data = [];
		for i in images:
			likes = Likes.objects.all().filter(imageId = i.id);
			likedata = [];
			for like in likes:
				likedata.append(like.username);

			thumb = Functions.getThumbnail_b64(i.path);
			thumbdata = thumb.decode("utf-8");
			item = {
				Constants.getCode("dPostId")      : i.id,
				Constants.getCode("dPath")        : i.path,	#'path'
				Constants.getCode("dDescription") : i.desc,	#'description'
				Constants.getCode("dUsername")    : i.owner,	#'username'
				Constants.getCode("dLikes")	  : likedata,
				Constants.getCode("dTimestamp")   : i.ctime.__str__(),
				Constants.getCode("dB64string")   : thumbdata,	#'b64string'
			       };

			data.append(item);

		if(len(data) == 0):
			return HttpResponse(Constants.getCode("ecode_noFeeds"));

		return HttpResponse(json.dumps(data));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


# fetch_feeds is used to fetch posts for the user feed page.
# It fetches only a certain number of posts at a time.
# The number is defined in Constants (feedBatchCount).
# It fetches feeds from only followed users.
# The feeds are fetched from the timestamp given. If no timestamp is given
# the function fetches from current timestamp.
def fetch_feeds(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		timestamp = request.POST.get(Constants.getCode("uTimestamp"), '');

		# get list of followed users
		followlist = Follows.objects.all().filter(follower = username).filter(fstatus = "accepted");
		if followlist.count() == 0:
			return HttpResponse(Constants.getCode("ecode_noFollowing"));

		userlist = [];
		for user in followlist:
			userlist.append(user.followee)

		# check if timestamp is given
		if(timestamp == '' or timestamp == 'null'):
			images = Images.objects.all().filter(owner__in=userlist).order_by('-ctime')[:Constants.feedBatchCount];
		else:
			images = Images.objects.all().filter(owner__in=userlist).filter(ctime__lt=timestamp).order_by('-ctime')[:Constants.feedBatchCount];

		data = [];
		for i in images:
			likes = Likes.objects.all().filter(imageId = i.id);
			likedata = [];
			for like in likes:
				likedata.append(like.username);

			image = Functions.getImage_b64(i.path);
			imagedata = image.decode("utf-8");

			item = {
				Constants.getCode("dPostId")      : i.id,
				Constants.getCode("dPath")        : i.path,	#'path'
				Constants.getCode("dDescription") : i.desc,	#'description'
				Constants.getCode("dUsername")    : i.owner,	#'username'
				Constants.getCode("dLikes")	  : likedata,
				Constants.getCode("dTimestamp")   : i.ctime.__str__(),
				Constants.getCode("dB64string")   : imagedata,	#'b64string'
			       };

			data.append(item);

		if(len(data) == 0):
			return HttpResponse(Constants.getCode("ecode_noFeeds"));

		return HttpResponse(json.dumps(data));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


# fetch_post() is used to fetch details of a certain post.
# the post is identified using the postId received from the user app.
def fetch_post(request):
	if request.method == "POST":
		postId = request.POST.get(Constants.getCode("uPostId"), '');

		post = Images.objects.get(pk = postId);
		image = Functions.getImage_b64(post.path);
		imagedata = image.decode("utf-8");

		item = {
			Constants.getCode("dPostId")      : post.id,
			Constants.getCode("dPath")        : post.path,	#'path'
			Constants.getCode("dDescription") : post.desc,	#'description'
			Constants.getCode("dUsername")    : post.owner,	#'username'
			Constants.getCode("dTimestamp")   : post.ctime.__str__(),
			Constants.getCode("dB64string")   : imagedata	#'b64string'
		       };

		return HttpResponse(json.dumps(item));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

# fetch_profile() is used to fetch details of a user profile.
# The profile is identified using the username.
# Only followed profiles can be fetched.
# TODO add access for public users.
def fetch_profile(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		profileId = request.POST.get(Constants.getCode("uProfileId"), '');

		try:
			user = User.objects.get(username = profileId);
			follows = Follows.objects.get(followee = profileId, follower = username);

			if not follows:
				return HttpResponse(Constants.getCode("ecode_notFollowing"));

			data = {};
			data[Constants.getCode("dProfileId")] = profileId;

			images = Images.objects.all().filter(owner = profileId);

			# create image thumbnails and add to data list.
			idata = [];
			for i in images:
				image = Functions.getThumbnail_b64(i.path);
				imagedata = image.decode("utf-8");

				item = {
					Constants.getCode("dPostId")      : i.id,
					Constants.getCode("dPath")        : i.path,	#'path'
					Constants.getCode("dDescription") : i.desc,	#'description'
					Constants.getCode("dUsername")    : i.owner,	#'username'
					Constants.getCode("dTimestamp")   : i.ctime.__str__(),
					Constants.getCode("dB64string")   : imagedata	#'b64string'
				       };
				idata.append(item);

			if(len(idata) == 0):
				data[Constants.getCode("dThumbs")] = Constants.getCode("ecode_noFeeds");
			else:
				data[Constants.getCode("dThumbs")] = idata;

			return HttpResponse(json.dumps(data));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchUser"));
		except Follows.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_notFollowing"));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

# fetch_requests() is used to get list of unaccepted requests.
def fetch_requests(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');

		rows = Follows.objects.all().filter(followee = username, fstatus = "requested");
		requests = [];

		for row in rows:
			item = {
				Constants.getCode("dFollower") : row.follower,
				Constants.getCode("dFollowStatus") : row.fstatus,
			};
			requests.append(item);

		if(len(requests) == 0):
			return HttpResponse(Constants.getCode("ecode_noRequests"));
		else:
			return HttpResponse(json.dumps(requests));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


