#
#	Like Functions
#
#	This file contains basic functions used for the like system.
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


# likes_post() is used to register a like for a post.
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


# unlikes_post() is used to unregister the like for a post.
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

