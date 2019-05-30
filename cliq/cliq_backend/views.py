from django.http import HttpResponse;
from django.db import IntegrityError;
from cliq_backend.models import User, Images;
import codes;
import random;
import base64;
import json;

def index(request):
	return HttpResponse("Hello World!");

def register(request):
	if(request.method == "POST"):
		username = request.POST.get(codes.username_post, "");
		if(username == ""):
			return HttpResponse(codes.empty_username);

		try:
			lk = abs(hash("asdf" + str(random.randint(1, 10))));
			u = User(username = username, lastkey = lk);
			u.save();
			var = { 'username':username, 'lastkey':lk };
			return HttpResponse(json.dumps(var));
		except IntegrityError as e:
			return HttpResponse(codes.username_already_exists);
	else:
		return HttpResponse(codes.not_post);

def image_upload(request):
	if request.method == "POST":
		username = request.POST.get("username", '');
		path = "images/"+username;
		b64 = request.POST.get("image", 'nil');
		desc = request.POST.get("desc", "");
		afile = open(path, 'wb');
		decoded = base64.b64decode(b64);
		afile.write(decoded);
		afile.close();

		try:
			i = Images(path = path, desc = desc, owner = username);
			i.save();
			retval = { 'status':'ok', 'id':i.id };
			return HttpResponse(json.dumps(retval));
		except IntegrityError as e:
			return HttpResponse("errocc");
	else:
		return HttpResponse(codes.not_post);
