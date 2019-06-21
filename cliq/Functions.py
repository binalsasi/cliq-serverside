#
#	Functions.py
#
#	This file contains functions such as image saving and thumbnail 
#	generation.
#
#	This app uses Google Cloud Platform App Engine as host
# 	So some codes are written to work with GCP.
#


import glob;
from PIL import Image;
import Constants;
import base64;
from google.cloud import storage
from io import BytesIO;

thumbsize = 128;
thumbprefix = "T_";


# read() is used to read from GCP bucket
def read(directory, filename):
	storage_client = storage.Client();
	bucket = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	ret = blob.download_as_string();
	
	return ret;

# write() is used to write to GCP bucket
def write(directory, filename, data):
	storage_client = storage.Client();
	bucket = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	blob.upload_from_string(data);

# generateThumbnail() reads base64 image, converts to PIL.image then resizes
# and saves the thumbnail.
def generateThumbnail(filename):
	bytes = read(Constants.dir_image, filename);
	decoded = base64.b64decode(bytes);

	image = Image.open(BytesIO(decoded));
	image.thumbnail((Constants.thumbsize, Constants.thumbsize), Image.ANTIALIAS);

	buffered = BytesIO();
	image.save(buffered, format = Constants.thumbnail_format);

	b64 = base64.b64encode(buffered.getvalue());
	#b64 = base64.b64encode(image.tobytes());

	write(Constants.dir_thumbs, Constants.thumbprefix + filename, b64);

# getThumbnail() gets thumbnail base64 and returns as it is.
def getThumbnail_b64(filename):
	bytes = read(Constants.dir_thumbs, Constants.thumbprefix + filename);
	return bytes;

# saveImage_b64 is used to save image as base64 string
def saveImage_b64(filename, b64):
	write(Constants.dir_image, filename, b64);

# getImage_b64 reads the image saved (as base64) and returns it.
def getImage_b64(filename):
	bytes = read(Constants.dir_image, filename);
	return bytes;







# the following functions behave similar to the ones above.
# the following functions are used for local testing.
# In case, the app is to be used for local usage, 
#    use the following functions,
#    instead of the funcions above.


def readx(directory, filename):
	image = open(directory + filename, "r");
	ret = image.read();
	image.close();
	
	return ret;

def writex(directory, filename, data):
	path = directory + filename;
	afile = open(path, 'w');
	afile.write(data);
	afile.close();

def getThumbnail_b64x(filename):
	bytes = readx(Constants.dir_thumbs, Constants.thumbprefix + filename);
	return str.encode(bytes);

def saveImage_b64x(filename, b64):
	print(type(b64));
	writex(Constants.dir_image, filename, b64);

def getImage_b64x(filename):
	bytes = readx(Constants.dir_image, filename);
	return str.encode(bytes);

def generateThumbnailx(filename):
	bytes = readx(Constants.dir_image, filename);
	decoded = base64.b64decode(bytes);

	image = Image.open(BytesIO(decoded));
	image.thumbnail((Constants.thumbsize, Constants.thumbsize), Image.ANTIALIAS);

	buffered = BytesIO();
	image.save(buffered, format = Constants.thumbnail_format);

	b64 = base64.b64encode(buffered.getvalue());
	b64 = b64.decode("utf-8");
	#b64 = base64.b64encode(image.tobytes());
	print(type(b64));

	writex(Constants.dir_thumbs, Constants.thumbprefix + filename, b64);
