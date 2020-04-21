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
]