#
#	Basic Functions
#
#	This file contains apis for basic functionalities.
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


# index is not used, it remains for basic testing.
def index(request):
	return HttpResponse(Constants.getCode("OK"));

# code base is defined in Constants which contains the error codes and their values.
# code base is sent to user app and used so that error codes doesn't have to be
# re written in the app.
def fetch_code_base(request):
	return HttpResponse(json.dumps(Constants.codebase));


# register() is used for one time registration of user with the app.
# At the moment it is pretty basic, only accepts a username.
# It will be rewritted to work with google, facebook and other sign in techniques.

# register() adds the username and a key to the database. This key (in a future implementation)
# will be used to encrypt traffic.
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




# image_upload() is used to save image (received as base64 string) and generate
# a thumbnail for the image for faster previewing.

# the definitions for saving is defined in Functions.py
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


# search_username() is used to find some usernames for client's search key.
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

# discover_people() returns a list of usernames that client may like to follow.
# At the moment it returns only a list of usernames.
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
