from django.urls import path
from . import api_views

app_name = "api_forum"

urlpatterns = [
    path('verify-email/', api_views.verify_email, name='verify-email'),
    path('verify-username/', api_views.verify_username, name='verify-username'),
    path('like-toggle/', api_views.like_toggle, name='like-toggle'),
]
