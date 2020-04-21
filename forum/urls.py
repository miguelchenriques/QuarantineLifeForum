from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('<slug:slug>/', views.topic_details, name='topic'),
    path('<int:post_id>/', views.post_details, name='post')
]