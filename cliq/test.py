import Constants;
import base64;

thumbprefix = "T_";
filename = "testuser1_2019-06-04_2";
with open(Constants.dir_thumbs + thumbprefix + filename, "rb") as thumb:
	content = thumb.read();
	b64 = base64.b64encode(content)
	print(b64);
