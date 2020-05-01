from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'forum'
urlpatterns = [
    # Forum URLS
    path('', views.homepage, name='home'),
    path('topic_<slug:slug>/', views.topic_details, name='topic'),
    path('post_<int:post_id>/', views.post_details, name='post'),

    # Accounts URLS
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # API URLS
    path('api/verify-email/', views.verify_email, name='api_verify_email'),
    path('api/verify-username/', views.verify_username, name='api_verify_username'),
    path('api/like_toggle/', views.like_toggle, name='api_like_toggle'),
    path('api/new_comment/<int:post_id>/', views.new_comment, name='api_new_comment'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/signup', views.signup_api, name='api_signup'),
]