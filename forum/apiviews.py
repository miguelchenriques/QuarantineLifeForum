from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from .forms import LogInForm, UserSignUpForm, PostForm
from .models import Comment, Post, Profile, Topic
from datetime import datetime


@require_GET
def verify_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists(),
    }
    return JsonResponse(data)


@require_GET
def verify_username(request):
    username = request.GET.get('username')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@require_POST
@login_required
def like_toggle(request):
    user = request.user
    post = get_object_or_404(Post, pk=request.POST['article_id'])
    if post.user_has_like(user):
        post.post_pizzas.remove(user)
        has_like = False
    else:
        post.post_pizzas.add(user)
        has_like = True
    data = {
        'article_id': request.POST['article_id'],
        'has_like': has_like,
        'like_count': post.post_pizzas.all().count(),
    }
    return JsonResponse(data)


@require_POST
@login_required
def new_comment(request):
    post_id = request.POST['post_id']
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    comment = Comment(post=post, owner=user, pub_date=timezone.now(), text=request.POST['text'])
    comment.save()

    date = datetime.strftime(comment.pub_date, "%d-%m-%Y-%H-%M-%p")

    response = {
        'owner_username': comment.owner.username,
        'post_id': post_id,
        'id': comment.id,
        'text': comment.text,
        'num_pizzas': comment.num_likes(),
        'pub_date': date,
        'owner_image': comment.owner.profile.profile_image
    }

    return JsonResponse(response)


@require_POST
def login_api(request):
    form = LogInForm(data=request.POST)
    response = {
        'login_successful': False
    }
    print(form.is_bound)
    if form.is_valid():
        form.clean()
        login(request, form.get_user())
        response['login_successful'] = True

    return JsonResponse(response)


@require_POST
def signup_api(request):
    response = {
        'signup_successful': False
    }
    form = UserSignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        response['signup_successful'] = True
        Profile(user=user).save()
    return JsonResponse(response)


@require_POST
@login_required
def create_post_api(request):
    topic_id = request.POST['topic_id']
    topic = get_object_or_404(Topic, id=topic_id)
    post = Post(owner=request.user, pub_date=timezone.now(), topic=topic)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        form.save()
        response = {
            'created': True,
            'id': post.id,
            'owner': post.owner.username,
            'topic': topic.slug,
            'title': post.title,
            'text': post.text,
            'pub_date': post.pub_date,
            'image': post.image,
            'video': post.video
        }
    else:
        response = {'created': False}

    return JsonResponse(response)


@require_GET
def login_required_api(request):
    response = {
        'is_authenticated': False
    }
    if request.user.is_authenticated:
        response['is_authenticated'] = True
    return JsonResponse(response)


@require_POST
@login_required
def follow_topic_api(request):
    topic = get_object_or_404(Topic, id=request.POST['topic_id'])
    response = {
        'is_following': False
    }
    if topic.is_following(request.user):
        topic.followers.remove(request.user)
    else:
        topic.followers.add(request.user)
        response['is_following'] = True
    response['num_followers'] = topic.num_followers()
    return JsonResponse(response)


@require_POST
@login_required
def comment_like_toggle(request):
    user = request.user
    comment = get_object_or_404(Comment, pk=request.POST['article_id'])
    if comment.user_has_like(user):
        comment.comment_pizzas.remove(user)
        has_like = False
    else:
        comment.comment_pizzas.add(user)
        has_like = True
    data = {
        'article_id': request.POST['article_id'],
        'has_like': has_like,
        'like_count': comment.comment_pizzas.all().count(),
    }
    return JsonResponse(data)
