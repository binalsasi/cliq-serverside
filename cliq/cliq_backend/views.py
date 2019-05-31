from django.http import HttpResponse;
from django.db import IntegrityError;
from cliq_backend.models import User, Images;
from datetime import datetime;
import Constants;
import random;
import base64;
import json;

def index(request):
	return HttpResponse(Constants.str_helloWorld);

def register(request):
	if(request.method == "POST"):
		username = request.POST.get(Constants.registration_uUsername, "");
		if(username == ""):
			return HttpResponse(Constants.ecode_emptyUsername);

		try:
			lk = abs(hash(username + str(random.randint(1, 10))));
			u = User(username = username, lastkey = lk);
			u.save();
			var = { Constants.registration_dUsername:username, Constants.registration_dKey:lk };
			return HttpResponse(json.dumps(var));
		except IntegrityError as e:
			return HttpResponse(Constants.ecode_usernameAlreadyExists);
	else:
		return HttpResponse(Constants.ecode_notPost);

def image_upload(request):
	if request.method == "POST":
		username = request.POST.get(Constants.imageUpload_uUsername, '');
		count = Images.objects.filter(owner=username).count();
		cur_date  = datetime.today().strftime(Constants.format_date);
		path = Constants.dir_image + username + "_" + str(cur_date) + "_" + str(count);

		b64 = request.POST.get(Constants.imageUpload_uImage, 'nil');
		#handle null image
		desc = request.POST.get(Constants.imageUpload_uDescription, "");
		afile = open(path, 'wb');
		decoded = base64.b64decode(b64);
		afile.write(decoded);
		afile.close();

		#check if saving was successful. handle cases

		try:
			i = Images(path = path, desc = desc, owner = username);
			i.save();
			retval = { Constants.imageUpload_dStatus:Constants.str_ok, Constants.imageUpload_dId:i.id };
			return HttpResponse(json.dumps(retval));
		except IntegrityError as e:
			return HttpResponse(Constants.ecode_imageExists);
	else:
		return HttpResponse(Constants.ecode_notPost);
