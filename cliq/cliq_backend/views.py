#
#	view.py
#
#	This file is the consolidation of all *_functions.py
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

def index(request):
	return HttpResponse(Constants.getCode("OK"));


def fetch_code_base(request):
	return HttpResponse(json.dumps(Constants.codebase));




def register(request):
	if(request.method == "POST"):

		username = request.POST.get(Constants.getCode("uUsername"), "");

		if(username == ""):
			return HttpResponse(Constants.getCode("ecode_emptyUsername"));

		try:
			lk = abs(hash(username + str(random.randint(1, 10))));

			u = User(username = username, lastkey = lk);
			u.save();

			var = {
				Constants.getCode("dUsername") : username,
				Constants.getCode("dKey")      : lk
			      };

			return HttpResponse(json.dumps(var));

		except IntegrityError as e:
			return HttpResponse(Constants.getCode("ecode_usernameAlreadyExists"));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def image_upload(request):
	if request.method == "POST":

		username = request.POST.get(Constants.getCode("uUsername"), '');
		count    = Images.objects.filter(owner=username).count();
		cur_date = datetime.today().strftime(Constants.format_date);
		filepath = username + "_" + str(cur_date) + "_" + str(count);

		b64      = request.POST.get(Constants.getCode("uImage"), 'nil');

		#handle null image
		desc = request.POST.get(Constants.getCode("uDescription"), "");

		Functions.saveImage_b64(filename = filepath, b64 = b64);
		#check if saving was successful. handle cases

		try:
			i = Images(path = filepath, desc = desc, owner = username);
			i.save();

			retval = {
					Constants.getCode("dStatus") : Constants.getCode("OK"),
					Constants.getCode("dId")     : i.id
				 };

			Functions.generateThumbnail(filepath);

			return HttpResponse(json.dumps(retval));

		except IntegrityError as e:
			return HttpResponse(Constants.getCode("ecode_imageExists"));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


def fetch_home(request):
	if request.method == "POST":

		username = request.POST.get(Constants.getCode("uUsername"), '');

#		try:
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
#		except 

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def fetch_feeds(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		timestamp = request.POST.get(Constants.getCode("uTimestamp"), '');

		followlist = Follows.objects.all().filter(follower = username).filter(fstatus = "accepted");
		if followlist.count() == 0:
			return HttpResponse(Constants.getCode("ecode_noFollowing"));

		userlist = [];
		for user in followlist:
			userlist.append(user.followee)

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

def fetch_profile(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		profileId = request.POST.get(Constants.getCode("uProfileId"), '');

		try:
			user = User.objects.get(username = profileId);
			follows = Follows.objects.get(followee = profileId, follower = username);

			if not follows:
				return HttpResponse((Constants.getCode("ecode_notFollowing"));

			data = {};
			data[Constants.getCode("dProfileId")] = profileId;

			images = Images.objects.all().filter(owner = profileId);

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

def follow_request(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		followee = request.POST.get(Constants.getCode("uFollowee"), '');

		if username == followee:
			return HttpResponse(Constants.getCode("ecode_noSelfFollow"));

		try:
			user = User.objects.get(username = followee);

			try:
				row = Follows.objects.get(follower = username, followee = followee);
				return HttpResponse(Constants.getCode("ecode_alreadyFollow"));

			except Follows.DoesNotExist:
				if user.privacy == "private":
					reqstatus = "requested";
				else
					reqstatus = "accepted";

				followRow = Follows(follower = username, followee = followee, fstatus = reqstatus);
				followRow.save();
				if not followRow:
					return HttpResponse(Constants.getCode("ecode_unableFollow"));
				else:
					return HttpResponse(Constants.getCode("OK"));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchUser"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def unfollow_request(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		followee = request.POST.get(Constants.getCode("uFollowee"), '');

		if username == followee:
			return HttpResponse(Constants.getCode("ecode_noSelfFollow"));

		try:
			user = User.objects.get(username = followee);

			try:
				row = Follows.objects.get(follower = username, followee = followee);
				row.delete();
				return HttpResponse(Constants.getCode("OK"));

			except Follows.DoesNotExist:
				return HttpResponse(Constants.getCode("ecode_notFollowed"));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchUser"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def get_followers_list(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		profileId = request.POST.get(Constants.getCode("uProfileId"), '');

		try:
			user = User.objects.get(username = profileId);

			rows = Follows.objects.all().filter(followee = profileId);
			followerlist = [];

			if username == profileId:
				for row in rows:
					item = {
						Constants.getCode("dFollower") : row.follower,
						Constants.getCode("dFollowStatus") : row.fstatus,
					};
					followerlist.append(item);
			else:
				for row in rows:
					item = {
						Constants.getCode("dFollower") : row.follower,
					};
					followerlist.append(item);

			if(len(followerlist) == 0):
				return HttpResponse(Constants.getCode("ecode_noFollowers"));
			else:
				return HttpResponse(json.dumps(followerlist));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchUser"));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));



def get_followings_list(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		profileId = request.POST.get(Constants.getCode("uProfileId"), '');

		try:
			user = User.objects.get(username = profileId);

			rows = Follows.objects.all().filter(follower = profileId);
			followinglist = [];

			if username == profileId:
				for row in rows:
					item = {
						Constants.getCode("dFollowee") : row.followee,
						Constants.getCode("dFollowStatus") : row.fstatus,
					};
					followinglist.append(item);
			else:
				for row in rows:
					item = {
						Constants.getCode("dFollowee") : row.followee,
					};
					followinglist.append(item);

			if(len(followinglist) == 0):
				return HttpResponse(Constants.getCode("ecode_noFollowers"));
			else:
				return HttpResponse(json.dumps(followinglist));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchUser"));

	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

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


def follow_request_action(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		follower = request.POST.get(Constants.getCode("uProfileId"), '');
		action   = request.POST.get(Constants.getCode("uAction"), '');

		try:
			row = Follows.objects.get(followee = username, follower = follower, fstatus = "requested");

			if action == "accept":
				row.fstatus = "accepted";
				row.save();

			elif action == "decline":
				row.delete();

			else :
				return HttpResponse(Constants.getCode("ecode_badAction"));

			return HttpResponse(Constants.getCode("OK"));

		except Follows.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noRequest"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def search_username(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		searchkey = request.POST.get(Constants.getCode("uSearchKey"), '');

		try:
			results = User.objects.all().filter(username__icontains=searchkey).filter(~Q(username = username));
			if(results.count() == 0):
				return HttpResponse(Constants.getCode("ecode_noResult"));

			data = [];
			for user in results:
				data.append(user.username);

			return HttpResponse(json.dumps(data));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noResult"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


def likes_post(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		postId   = request.POST.get(Constants.getCode("uPostId"), '');

		try:
			post = Images.objects.get(id=postId);

			try:
				like = Likes.objects.get(imageId = postId, username = username);
				return HttpResponse(Constants.getCode("ecode_alreadyLiked"));
			except Likes.DoesNotExist as e:
				like = Likes(imageId = postId, username = username);
				like.save();
				if not like:
					return HttpResponse(Constants.getCode("ecode_unableToLike"));
				else:
					return HttpResponse(Constants.getCode("OK"));

		except Images.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchPost"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));


def unlikes_post(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		postId   = request.POST.get(Constants.getCode("uPostId"), '');

		try:
			post = Images.objects.get(id=postId);

			try:
				like = Likes.objects.get(imageId = postId, username = username);
				like.delete();
				return HttpResponse(Constants.getCode("OK"));

			except Likes.DoesNotExist as e:
				return HttpResponse(Constants.getCode("ecode_notLiked"));

		except Images.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchPost"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def discover_people(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');

		try:
			users = User.objects.all().filter(~Q(username=username))[:Constants.discoverPeopleCount];

			data = [];
			for user in users:
				data.append(user.username);

			if(len(data) == 0):
				return HttpResponse(Constants.getCode("ecode_noUser"));

			return HttpResponse(json.dumps(data));

		except User.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noUser"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def add_comment(request):
	if request.method == "POST":
		username = request.POST.get(Constants.getCode("uUsername"), '');
		postId   = request.POST.get(Constants.getCode("uPostId"), '');
		comment  = request.POST.get(Constants.getCode("uText"), '');

		try:
			post = Images.objects.get(id=postId);

			comment = Comments(imageId = postId, username = username, comment = comment);
			comment.save();
			if not comment:
				return HttpResponse(Constants.getCode("ecode_unableToComment"));
			else:
				return HttpResponse(Constants.getCode("OK"));

		except Images.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchPost"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def remove_comment(request):
	if request.method == "POST":
		username  = request.POST.get(Constants.getCode("uUsername"), '');
		postId    = request.POST.get(Constants.getCode("uPostId"), '');
		commentId = request.POST.get(Constants.getCode("uCommentId"), '');

		try:
			post = Images.objects.get(id=postId);

			try:
				comment = Comments.objects.get(id=commentId);
				commentTime = comment.ctime;
				currentTime = datetime.now();
				difference = currentTime - commentTime;
				if(difference.seconds > maxDeletePeriodinSeconds):
					return HttpResponse(Constants.getCode("ecode_tooLate"));

				comment.delete();
				return HttpResponse(Constants.getCode("OK"));

			except Comments.DoesNotExist as e:
				return HttpResponse(Constants.getCode("ecode_noSuchComment"));

		except Images.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchPost"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));

def get_comments(request):
	if request.method == "POST":
		username  = request.POST.get(Constants.getCode("uUsername"), '');
		postId    = request.POST.get(Constants.getCode("uPostId"), '');

		try:
			post = Images.objects.get(id=postId);

			try:
				comments = Comments.objects.all().filter(imageId = postId).order_by("-ctime");

				data = [];
				for comment in comments:
					item = {
						Constants.getCode("dCommentId"): comment.id,
						Constants.getCode("dUsername"):  comment.username,
						Constants.getCode("dText"):      comment.comment,
						Constants.getCode("dTimestamp"): comment.ctime.__str__(),
					};
					data.append(item);

				if(len(data) == 0):
					return HttpResponse(Constants.getCode("ecode_noComments"));

				return HttpResponse(json.dumps(data));

			except Comments.DoesNotExist as e:
				return HttpResponse(Constants.getCode("ecode_noComments"));

		except Images.DoesNotExist as e:
			return HttpResponse(Constants.getCode("ecode_noSuchPost"));
	else:
		return HttpResponse(Constants.getCode("ecode_notPost"));
