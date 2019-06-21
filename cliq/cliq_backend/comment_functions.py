#
#	Comment Functions
#
#	This file contains basic functions used for comment CRUD.
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


# add_comment() adds a comment to the Comments table
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


# remove_comment() allows removal of comment from the Comments Table, if
# the comment is less than 10 minutes (or maxDeletePeriod) of age.
# remove_comment() is not yet implemented in front end (at the time of writing).
def remove_comment(request):
	if request.method == "POST":
		username  = request.POST.get(Constants.getCode("uUsername"), '');
		postId    = request.POST.get(Constants.getCode("uPostId"), '');
		commentId = request.POST.get(Constants.getCode("uCommentId"), '');

		try:
			post = Images.objects.get(id=postId);

			try:
				comment = Comments.objects.get(id=commentId);


				# check if comment is 10 minutes (or maxDeletePeriod) of age.
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


# get_comments() is used to get comments for a post.
# TODO need to check post privacy
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
