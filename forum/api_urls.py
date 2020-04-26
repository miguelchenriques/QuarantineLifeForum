from django.urls import path
from . import api_views

app_name = "api_forum"

urlpatterns = [
    path('verify-email/', api_views.verify_email, name='verify_email'),
    path('verify-username/', api_views.verify_username, name='verify_username'),
    path('like_toggle/', api_views.like_toggle, name='like_toggle'),
    path('new_comment/<int:post_id>', api_views.new_comment, name='new_comment'),
]
