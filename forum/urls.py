from django.urls import path
from . import views, apiviews
from django.contrib.auth import views as auth_views

app_name = 'forum'
urlpatterns = [
    # Forum URLS
    path('', views.homepage, name='home'),
    path('topic_<slug:slug>/', views.topic_details, name='topic'),
    path('post_<int:post_id>/', views.post_details, name='post'),
    path('search/', views.search, name='search'),

    # Accounts URLS
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # API URLS
    path('api/verify-email/', apiviews.verify_email, name='api_verify_email'),
    path('api/verify-username/', apiviews.verify_username, name='api_verify_username'),
    path('api/like_toggle/', apiviews.like_toggle, name='api_like_toggle'),
    path('api/new_comment/<int:post_id>/', apiviews.new_comment, name='api_new_comment'),
    path('api/login/', apiviews.login_api, name='api_login'),
    path('api/signup', apiviews.signup_api, name='api_signup'),
]