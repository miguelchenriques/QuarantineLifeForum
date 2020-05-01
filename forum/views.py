from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Topic, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CommentForm, TopicForm, UserSignUpForm, LogInForm
from django.core.exceptions import ValidationError

page_size = 10


# Common context
def accounts_form_context(request):
    context = {
        'loginForm': LogInForm(),
        'signupForm': UserSignUpForm()
    }
    return context


# Forum display Views
def homepage(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, page_size)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'page_list': page_list,
    }
    return render(request, 'forum/home.html', context)


def topic_details(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    post_list = Post.objects.filter(topic=topic)
    paginator = Paginator(post_list, page_size)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'topic': topic,
        'page_list': page_list
    }
    return render(request, 'forum/topic_details.html', context)
    # return None


def post_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'forum/post_details.html', context)
    # return None


def popular_topics(request):
    topic_list = Topic.objects.annotate(followrs_count=Count('followers')).orderBy('-followers_count')
    paginator = Paginator(topic_list, page_size)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'page_list': page_list,
    }
    # return render(request, 'forum/popular_topics.html', context)
    return None


@login_required
def create_Topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:home')
    return None


def get_page(page_number, paginator):
    try:
        page_list = paginator.page(page_number)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator(paginator.num_pages)

    return page_list


# Authentication Views
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('forum:home')
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# API VIEWS
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
    return JsonResponse(response)
