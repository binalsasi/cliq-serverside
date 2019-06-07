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
		filepath = username + "_" + str(cur_date) + "_" + str(count);

		b64 = request.POST.get(Constants.imageUpload_uImage, 'nil');
		#handle null image
		desc = request.POST.get(Constants.imageUpload_uDescription, "");
		Functions.saveImage_b64(filename = filepath, b64 = b64);
		#check if saving was successful. handle cases

		try:
			i = Images(path = filepath, desc = desc, owner = username);
			i.save();
			retval = { Constants.imageUpload_dStatus:Constants.str_ok, Constants.imageUpload_dId:i.id };

			Functions.generateThumbnail(filepath);
			return HttpResponse(json.dumps(retval));
		except IntegrityError as e:
			return HttpResponse(Constants.ecode_imageExists);
	else:
		return HttpResponse(Constants.ecode_notPost);


def fetch_home(request):
	if request.method == "POST":
		username = request.POST.get(Constants.fetchHome_uUsername, '');
#		try:
		images = Images.objects.filter(owner=username);
		data = [];
		for i in images:
			thumb = Functions.getThumbnail_b64(i.path);
			thumbdata = thumb.decode("utf-8");
			item = { 'path':i.path, 'description':i.desc, 'username' : i.owner, 'b64string' : thumbdata };
			data.append(item);

		if(len(data) == 0):
			return HttpResponse(Constants.ecode_noFeeds);

		return HttpResponse(json.dumps(data));
#		except 
	else:
		return HttpResponse(Constants.ecode_notPost);

def fetch_feeds(request):
	if request.method == "POST":
		username = request.POST.get(Constants.fetchHome_uUsername, '');
		images = Images.objects.filter(~Q(owner=username));
		data = [];
		for i in images:
			thumb = Functions.getImage_b64(i.path);
			thumbdata = thumb.decode("utf-8");
			item = { 'path':i.path, 'description':i.desc, 'username' : i.owner, 'b64string' : thumbdata };
			data.append(item);
		if(len(data) == 0):
			return HttpResponse(Constants.ecode_noFeeds);

		return HttpResponse(json.dumps(data));
	else:
		return HttpResponse(Constants.ecode_notPost);

def fetch_thumb(request):
	if request.method == "POST":
		path = request.POST.get("path", "");
		try:
			with open(path, "rb") as f:
				return HttpResponse(f.read(), content_type="image/jpeg")
		except IOError:
			red = Image.new('RGBA', (1, 1), (255,0,0,0))
			response = HttpResponse(content_type="image/jpeg")
			red.save(response, "JPEG")
			return response;

def explicit_app_engine(request):
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    return HttpResponse(str(buckets));

#explicit_app_engine("zinc-advice-242819");

def create_bucketa(request):
	from google.cloud import storage;
	storage_client = storage.Client();
	bucket = storage_client.create_bucket("cliq_backend_8756473iasuh_bucket1");
	return HttpResponse("Bucket created name : " + bucket.name);
