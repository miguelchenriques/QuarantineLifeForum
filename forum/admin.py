from django.contrib import admin
from .models import Topic, Post

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass