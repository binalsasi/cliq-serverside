from django.db import models

class User(models.Model):
	username = models.CharField(max_length = 30, unique = True);
	lastkey  = models.CharField(max_length = 64);
	ctime    = models.DateTimeField(auto_now_add = True);
	ltime    = models.DateTimeField(auto_now = True);

	def __str__(self):
		return self.username;

class Images(models.Model):
	path  = models.CharField(max_length = 512);
	desc  = models.CharField(max_length = 1024);
	owner = models.CharField(max_length = 30);
	ctime = models.DateTimeField(auto_now_add = True);

class Follows(models.Model):
	follower = models.CharField(max_length = 30);
	followee = models.CharField(max_length = 30);
