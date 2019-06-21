from django.db import models

# The User model is used to hold data about each user.
class User(models.Model):
	username = models.CharField(max_length = 30, unique = True);
	lastkey  = models.CharField(max_length = 64);
	ctime    = models.DateTimeField(auto_now_add = True);
	ltime    = models.DateTimeField(auto_now = True);
	privacy  = models.CharField(max_length = 30, default="private");

	def __str__(self):
		return self.username;

# Images model contains the post details.
class Images(models.Model):
	path  = models.CharField(max_length = 512);
	desc  = models.CharField(max_length = 1024);
	owner = models.CharField(max_length = 30);
	ctime = models.DateTimeField(auto_now_add = True);

# Follows model contains the follow requests
class Follows(models.Model):
	follower = models.CharField(max_length = 30);
	followee = models.CharField(max_length = 30);
	fstatus  = models.CharField(max_length = 10);
	ctime = models.DateTimeField(auto_now_add = True);

# Likes model contains the likes for each post
class Likes(models.Model):
	imageId  = models.IntegerField();
	username = models.CharField(max_length = 30);
	ctime = models.DateTimeField(auto_now_add = True);

# Comments model contains the comments for each post.
class Comments(models.Model):
	imageId  = models.IntegerField();
	username = models.CharField(max_length = 30);
	comment  = models.TextField();
	ctime    = models.DateTimeField(auto_now_add = True);
