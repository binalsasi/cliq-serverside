from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('image_upload', views.image_upload, name='image_upload'),
	path('register', views.register, name='register'),
	path('fetch_home', views.fetch_home, name='fetch_home'),
	path('fetch_thumb', views.fetch_thumb, name='fetch_thumb'),
	path('fetch_feeds', views.fetch_feeds, name='fetch_feeds'),
	path('create_bucketa', views.create_bucketa, name='create_bucketa'),
	path('explicit_app_engine', views.explicit_app_engine, name='explicit_app_engine'),
	
]
