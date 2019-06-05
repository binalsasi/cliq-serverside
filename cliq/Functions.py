import glob;
from PIL import Image;
import Constants;
import base64

thumbsize = 128;
thumbprefix = "T_";
def generateThumbnail(filename):
	global thumbsize;
	global thumbprefix;
	image = Image.open(Constants.dir_image + filename);
	image.thumbnail((thumbsize, thumbsize), Image.ANTIALIAS);
	image.save(Constants.dir_thumbs + thumbprefix + filename, "JPEG");

def getThumbnail_b64(filename):
	global thumbprefix;
	with open(Constants.dir_thumbs + thumbprefix + filename, "rb") as thumb:
		content = thumb.read();
		b64 = base64.b64encode(content)
		return b64;

def saveImage_b64(filename, b64):
	path = Constants.dir_image + filename;
	afile = open(path, 'wb');
	decoded = base64.b64decode(b64);
	afile.write(decoded);
	afile.close();

def getImage_b64(filename):
	with open(Constants.dir_image + filename, "rb") as image:
		b64 = base64.b64encode(image.read());
		return b64;
