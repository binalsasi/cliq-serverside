from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('image_upload', views.image_upload, name='image_upload'),
	path('register', views.register, name='register'),
	path('fetch_home', views.fetch_home, name='fetch_home'),
	path('fetch_post', views.fetch_post, name='fetch_post'),
	path('fetch_feeds', views.fetch_feeds, name='fetch_feeds'),
	path('fetch_profile', views.fetch_profile, name='fetch_profile'),
]
