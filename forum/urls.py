from django.urls import path
from . import views, apiviews
from django.contrib.auth import views as auth_views

app_name = 'forum'
urlpatterns = [
    # Forum URLS
    path('', views.homepage, name='home'),
    path('topic_<slug:topic_slug>/', views.topic_details, name='topic'),
    path('post_<int:post_id>/', views.post_details, name='post'),
    path('search/', views.search, name='search'),
    path('popular_topics/', views.popular_topics, name='popular_topics'),

    # Accounts URLS
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/<str:username>', views.profile_detail, name="profile"),
    path('api/login/', apiviews.login_api, name='api_login'),
    path('api/signup', apiviews.signup_api, name='api_signup'),
    path('liked-posts/', views.liked_Posts, name='liked_posts'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # API URLS
    path('api/verify-email/', apiviews.verify_email, name='api_verify_email'),
    path('api/verify-username/', apiviews.verify_username, name='api_verify_username'),
    path('api/like_toggle/', apiviews.like_toggle, name='api_like_toggle'),
    path('api/new_comment/', apiviews.new_comment, name='api_new_comment'),
    path('api/new_post/', apiviews.create_post_api, name='api_new_post'),
    path('api/login_required/', apiviews.login_required_api, name='api_login_required'),
    path('api/topic_follow/', apiviews.follow_topic_api, name='api_follow_topic'),
    path('api/comment_like_toggle/', apiviews.comment_like_toggle, name='api_comment_like_toggle'),
    path('api/delete_post/', apiviews.delete_post_api, name='api_delete_post')
]
