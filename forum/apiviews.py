from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from .forms import CommentForm, LogInForm, UserSignUpForm
from .models import Comment, Post, Profile


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
    post = get_object_or_404(Post, pk=request.POST['post_id'])
    if post.user_has_like(user):
        post.post_pizzas.remove(user)
        has_like = False
    else:
        post.post_pizzas.add(user)
        has_like = True
    data = {
        'post_id': request.POST['post_id'],
        'has_like': has_like,
        'like_count': post.post_pizzas.all().count(),
    }
    return JsonResponse(data)


@require_POST
@login_required
def new_comment(request, post_id):
    post = get_object_or_404(pk=post_id)
    user = request.user
    comment = Comment(post=post, owner=user, pub_date=timezone.now())
    form = CommentForm(request.POST, instance=comment)
    form.save()

    response = {
        'owner_username': comment.owner.username,
        'post_id': post_id,
        'text': comment.text,
        'num_pizzas': comment.num_likes(),
        'pub_date': comment.pub_date,
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
