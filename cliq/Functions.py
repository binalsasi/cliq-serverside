import glob;
from PIL import Image;
import Constants;
import base64;
from google.cloud import storage

thumbsize = 128;
thumbprefix = "T_";

def read(directory, filename):
	storage_client = storage.Client();
	buckets = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	ret = blob.download_as_string();
	
	return ret;

def write(directory, filename, data):
	storage_client = storage.Client();
	buckets = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	blob.upload_from_string(data);


def generateThumbnail(filename):
	bytes = read(Constants.dir_image, filename);
	decoded = base64.b64decode(bytes);

	image = Image.open(io.BytesIO(decoded));
	image.thumbnail((Constants.thumbsize, Constants.thumbsize), Image.ANTIALIAS);

	byteIO = io.BytesIO();
	image.save(byteIO, Constants.thumbnail_format);
	byteArr = byteIO.getValue();

	b64 = base64.b64encode(byteArr);

	write(Constants.dir_thumbs, Constants.thumbprefix + filename, b64);


def getThumbnail_b64(filename):
	bytes = read(Constants.dir_thumb, Constants.thumbprefix + filename);
	return bytes;

def saveImage_b64(filename, b64):
	write(Constants.dir_image, filename, b64);

def getImage_b64(filename):
	bytes = read(Constants.dir_image, filename);
	return bytes;


















def generateThumbnailx(filename):
	global thumbsize;
	global thumbprefix;
	image = Image.open(Constants.dir_image + filename);
	image.thumbnail((thumbsize, thumbsize), Image.ANTIALIAS);
	image.save(Constants.dir_thumbs + thumbprefix + filename, "JPEG");

def getThumbnail_b64x(filename):
	global thumbprefix;
	with open(Constants.dir_thumbs + thumbprefix + filename, "rb") as thumb:
		content = thumb.read();
		b64 = base64.b64encode(content)
		return b64;

def saveImage_b64x(filename, b64):
	path = Constants.dir_image + filename;
	afile = open(path, 'wb');
	decoded = base64.b64decode(b64);
	afile.write(decoded);
	afile.close();

def getImage_b64x(filename):
	with open(Constants.dir_image + filename, "rb") as image:
		b64 = base64.b64encode(image.read());
		return b64;
