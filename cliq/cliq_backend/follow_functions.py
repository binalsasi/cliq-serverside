#
#	Follow Functions
#
#	This file contains basic functions used for the follow system.
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


# follow_request() is used to add follow request for a user.
# note : follower is the user who initiates the follow request
#    and followee is the user who gets the follow request.
# requests for public users are automatically accepted.
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
				else:
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


# unfollow_request() is used to unfollow a user.
# It does not notify the followee nor does it ask for followee's permission.
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


# get_followers_list() is used to get the list of followers for the given profileId.
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


# get_followings_list() is used to find list of followees
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



# follow_request_action() is used to accept/ decline a follow request.
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

