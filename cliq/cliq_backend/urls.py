from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('image_upload', views.image_upload, name='image_upload'),
	path('fetch_code_base', views.fetch_code_base, name='fetch_code_base'),
	path('register', views.register, name='register'),
	path('fetch_home', views.fetch_home, name='fetch_home'),
	path('fetch_post', views.fetch_post, name='fetch_post'),
	path('fetch_feeds', views.fetch_feeds, name='fetch_feeds'),
	path('fetch_profile', views.fetch_profile, name='fetch_profile'),
	path('follow_request', views.follow_request, name='follow_request'),
	path('unfollow_request', views.unfollow_request, name='unfollow_request'),
	path('get_followings_list', views.get_followings_list, name='get_followings_list'),
	path('get_followers_list', views.get_followers_list, name='get_followers_list'),
	path('fetch_requests', views.fetch_requests, name='fetch_requests'),
	path('follow_request_action', views.follow_request_action, name='follow_request_action'),
	path('search_username', views.search_username, name='search_username'),
	path('likes_post', views.likes_post, name='likes_post'),
	path('unlikes_post', views.unlikes_post, name='unlikes_post'),
]
