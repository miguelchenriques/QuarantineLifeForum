from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


# Create your models here.


class Topic(models.Model):
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    followers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="original_poster")
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title
