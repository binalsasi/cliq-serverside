from django.http import HttpResponse;
from django.db import IntegrityError;
from django.db.models import Q;
from cliq_backend.models import User, Images;
from datetime import datetime;
import Constants;
import random;
import base64;
import json;
import Functions;

def index(request):
	return HttpResponse(Constants.str_helloWorld);

def register(request):
	if(request.method == "POST"):

		username = request.POST.get(Constants.uUsername, "");

		if(username == ""):
			return HttpResponse(Constants.ecode_emptyUsername);

		try:
			lk = abs(hash(username + str(random.randint(1, 10))));

			u = User(username = username, lastkey = lk);
			u.save();

			var = {
				Constants.dUsername : username,
				Constants.dKey      : lk
			      };

			return HttpResponse(json.dumps(var));

		except IntegrityError as e:
			return HttpResponse(Constants.ecode_usernameAlreadyExists);

	else:
		return HttpResponse(Constants.ecode_notPost);

def image_upload(request):
	if request.method == "POST":

		username = request.POST.get(Constants.uUsername, '');
		count    = Images.objects.filter(owner=username).count();
		cur_date = datetime.today().strftime(Constants.format_date);
		filepath = username + "_" + str(cur_date) + "_" + str(count);

		b64      = request.POST.get(Constants.uImage, 'nil');

		#handle null image
		desc = request.POST.get(Constants.uDescription, "");

		Functions.saveImage_b64(filename = filepath, b64 = b64);
		#check if saving was successful. handle cases

		try:
			i = Images(path = filepath, desc = desc, owner = username);
			i.save();

			retval = {
					Constants.dStatus : Constants.str_ok,
					Constants.dId     : i.id
				 };

			Functions.generateThumbnail(filepath);

			return HttpResponse(json.dumps(retval));

		except IntegrityError as e:
			return HttpResponse(Constants.ecode_imageExists);

	else:
		return HttpResponse(Constants.ecode_notPost);


def fetch_home(request):
	if request.method == "POST":

		username = request.POST.get(Constants.uUsername, '');

#		try:
		images = Images.objects.filter(owner = username);

		data = [];
		for i in images:
			thumb = Functions.getThumbnail_b64(i.path);
			thumbdata = thumb.decode("utf-8");
			item = {
				Constants.dPostId      : i.id,
				Constants.dPath        : i.path,	#'path'
				Constants.dDescription : i.desc,	#'description'
				Constants.dUsername    : i.owner,	#'username'
				'leng': len(thumbdata),
				Constants.dB64string   : thumbdata,	#'b64string'
			       };

			data.append(item);

		if(len(data) == 0):
			return HttpResponse(Constants.ecode_noFeeds);

		return HttpResponse(json.dumps(data));
#		except 

	else:
		return HttpResponse(Constants.ecode_notPost);

def fetch_feeds(request):
	if request.method == "POST":
		username = request.POST.get(Constants.uUsername, '');
		timestamp = request.POST.get(Constants.uTimestamp, '');

		if(timestamp == '' or timestamp == 'null'):
			images = Images.objects.all().order_by('-ctime')[:Constants.feedBatchCount];
		else:
			images = Images.objects.all().filter(ctime__lt=timestamp).order_by('-ctime')[:Constants.feedBatchCount];

		data = [];
		for i in images:
			image = Functions.getImage_b64(i.path);
			imagedata = image.decode("utf-8");

			item = {
				Constants.dPostId      : i.id,
				Constants.dPath        : i.path,	#'path'
				Constants.dDescription : i.desc,	#'description'
				Constants.dUsername    : i.owner,	#'username'
				Constants.dTimestamp   : i.ctime,
				Constants.dB64string   : imagedata	#'b64string'
			       };

			data.append(item);

		if(len(data) == 0):
			return HttpResponse(Constants.ecode_noFeeds);

		return HttpResponse(json.dumps(data));
	else:
		return HttpResponse(Constants.ecode_notPost);


def fetch_post(request):
	if request.method == "POST":
		postId = request.POST.get(Constants.uPostId, '');

		post = Images.objects.get(pk = postId);
		image = Functions.getImage_b64(post.path);
		imagedata = image.decode("utf-8");

		item = {
			Constants.dPostId      : post.id,
			Constants.dPath        : post.path,	#'path'
			Constants.dDescription : post.desc,	#'description'
			Constants.dUsername    : post.owner,	#'username'
			Constants.dTimestamp   : i.ctime,
			Constants.dB64string   : imagedata	#'b64string'
		       };

		return HttpResponse(json.dumps(item));
	else:
		return HttpResponse(Constants.ecode_notPost);
