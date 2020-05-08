from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Topic(models.Model):
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    followers = models.ManyToManyField(User, blank=True, related_name='topic_followers')

    def __str__(self):
        return self.title

    def num_followers(self):
        return self.followers.count()

    def is_following(self, user):
        return self.followers.filter(username=user.username)


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    image = models.URLField(max_length=300, blank=True)
    video = models.URLField(max_length=300, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post_pizzas = models.ManyToManyField(User, related_name='post_likes', blank=True)
    pub_date = models.DateTimeField('Publication date')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.post_pizzas.count()

    def user_has_like(self, user):
        return self.post_pizzas.filter(username=user.username).exists()


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

    def user_has_like(self, user):
        return self.comment_pizzas.filter(username=user.username).exists()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(max_length=300, default='https://www.w3schools.com/w3images/avatar6.png')

    def __str__(self):
        return self.user.username

    def num_likes(self):
        count = 0
        posts = Post.objects.filter(owner=self.user)
        comments = Comment.objects.filter(owner=self.user)
        for post in posts:
            count += post.num_likes()
        for comment in comments:
            count += comment.num_likes()
        return count


