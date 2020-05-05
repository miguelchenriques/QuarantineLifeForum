from django.contrib import admin
from .models import Topic, Post, Comment, Profile


# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'num_followers']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ['title', 'topic', 'owner', 'pub_date', 'num_likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'owner', 'post', 'pub_date', 'num_likes']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_likes']
