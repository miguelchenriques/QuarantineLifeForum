from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Topic(models.Model):
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    followers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    def num_followers(self):
        return self.followers.count()


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    media = models.URLField(max_length=200, null=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="original_poster")
    post_pizzas = models.ManyToManyField(User, related_name='post_likes', blank=True)
    pub_date = models.DateTimeField('Publication date')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.post_pizzas.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    pub_date = models.DateTimeField(verbose_name='Comment Time')
    comment_pizzas = models.ManyToManyField(User, blank=True, related_name='comment_pizzas')

    class Meta:
        ordering = ['pub_date']

    def num_likes(self):
        return self.comment_pizzas.count()

    def __str__(self):
        return self.text
