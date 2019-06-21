from django.urls import path
from . import basic_functions, fetch_functions, follow_functions, like_functions, comment_functions

urlpatterns = [
	# basic_functions
	path('',                basic_functions.index,           name='index'),
	path('image_upload',    basic_functions.image_upload,    name='image_upload'),
	path('fetch_code_base', basic_functions.fetch_code_base, name='fetch_code_base'),
	path('register',        basic_functions.register,        name='register'),
	path('search_username', basic_functions.search_username, name='search_username'),
	path('discover_people', basic_functions.discover_people, name='discover_people'),

	# fetch_functions
	path('fetch_home',     fetch_functions.fetch_home,     name='fetch_home'),
	path('fetch_post',     fetch_functions.fetch_post,     name='fetch_post'),
	path('fetch_feeds',    fetch_functions.fetch_feeds,    name='fetch_feeds'),
	path('fetch_profile',  fetch_functions.fetch_profile,  name='fetch_profile'),
	path('fetch_requests', fetch_functions.fetch_requests, name='fetch_requests'),

	# follow_functions
	path('follow_request',        follow_functions.follow_request,        name='follow_request'),
	path('unfollow_request',      follow_functions.unfollow_request,      name='unfollow_request'),
	path('follow_request_action', follow_functions.follow_request_action, name='follow_request_action'),
	path('get_followings_list',   follow_functions.get_followings_list,   name='get_followings_list'),
	path('get_followers_list',    follow_functions.get_followers_list,    name='get_followers_list'),

	# like_functions
	path('likes_post',   like_functions.likes_post,   name='likes_post'),
	path('unlikes_post', like_functions.unlikes_post, name='unlikes_post'),

	# comment_functions
	path('add_comment',    comment_functions.add_comment,    name='add_comment'),
	path('remove_comment', comment_functions.remove_comment, name='remove_comment'),
	path('get_comments',   comment_functions.get_comments,   name='get_comments'),
]
