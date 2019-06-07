import glob;
from PIL import Image;
import Constants;
import base64;

bucket_name = "";

def getBucket():
	global bucket_name;
	bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name());

thumbsize = 128;
thumbprefix = "T_";

def read(filename):
	gcs_file = gcs.open(filename)
	contents = gcs_file.read()
	gcs_file.close()
	return contents;

def write(filename, mode, data):
	gcs_file = gcs.open(filename, mode);
	gcs_file.write(data)
	gcs_file.close()

def generateThumbnail(filename):
	global thumbsize;
	global thumbprefix;

	bytes = read("images/" + filename);
	image = Image.open(io.BytesIO(bytes));

	image.thumbnail((thumbsize, thumbsize), Image.ANTIALIAS);

	byteIO = io.BytesIO();
	image.save(byteIO, "JPEG");
	byteArr = byteIO.getValue();

	write("thumbs/T_"+filename, "wb", byteArr);



def getThumbnail_b64(filename):
	global thumbprefix;
	with open(Constants.dir_thumbs + thumbprefix + filename, "rb") as thumb:
		content = thumb.read();
		b64 = base64.b64encode(content)
		return b64;

def saveImage_b64(filename, b64):
	path = "images/" + filename;
	decoded = base64.b64decode(b64);
	write(path, "wb", decoded);

def getImage_b64(filename):
	with open(Constants.dir_image + filename, "rb") as image:
		b64 = base64.b64encode(image.read());
		return b64;


















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
