import glob;
from PIL import Image;
import Constants;
import base64;
from google.cloud import storage
from io import BytesIO;

thumbsize = 128;
thumbprefix = "T_";

def read(directory, filename):
	storage_client = storage.Client();
	bucket = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	ret = blob.download_as_string();
	
	return ret;

def write(directory, filename, data):
	storage_client = storage.Client();
	bucket = storage_client.get_bucket(Constants.bucket_name);
	blob = bucket.blob(directory + filename);

	blob.upload_from_string(data);


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


def getThumbnail_b64(filename):
	bytes = read(Constants.dir_thumbs, Constants.thumbprefix + filename);
	return bytes;

def saveImage_b64(filename, b64):
	write(Constants.dir_image, filename, b64);

def getImage_b64(filename):
	bytes = read(Constants.dir_image, filename);
	return bytes;















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



def getThumbnail_b64y(filename):
	global thumbprefix;
	with open(Constants.dir_thumbs + thumbprefix + filename, "rb") as thumb:
		content = thumb.read();
		b64 = base64.b64encode(content)
		return b64;

def saveImage_b64y(filename, b64):
	path = Constants.dir_image + filename;
	afile = open(path, 'wb');
	decoded = base64.b64decode(b64);
	afile.write(decoded);
	afile.close();

def getImage_b64y(filename):
	with open(Constants.dir_image + filename, "rb") as image:
		b64 = base64.b64encode(image.read());
		return b64;
