from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TopicForm, PostForm, EditProfileForm
from .models import Post, Topic, Profile

PAGE_SIZE = 10
MINIMUM_NUM_LIKES_TO_CREATE_TOPIC = 5


# Forum display Views
def homepage(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, PAGE_SIZE)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'page_list': page_list,
    }
    return render(request, 'forum/home.html', context)


def topic_details(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    post_list = Post.objects.filter(topic=topic)
    paginator = Paginator(post_list, PAGE_SIZE)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'topic': topic,
        'page_list': page_list,
        'postForm': PostForm()
    }
    return render(request, 'forum/topic_details.html', context)


def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'forum/post_details.html', context)


def popular_topics(request):
    topic_list = Topic.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')
    paginator = Paginator(topic_list, PAGE_SIZE)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'page_list': page_list,
    }
    return render(request, 'forum/popular_topics.html', context)


@login_required
def create_Topic(request):
    if request.user.profile.reputation() < MINIMUM_NUM_LIKES_TO_CREATE_TOPIC:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:home')
        else:
            return None


@require_GET
def search(request):
    query = request.GET['q']
    if query is not None:
        context = {
            'posts': Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)),
            'topics': Topic.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query)),
            'users': User.objects.filter(Q(username__icontains=query))
        }
        return render(request, 'forum/search.html', context)
    return redirect(request.META['HTTP_REFERER'])


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    topics_followed = Topic.objects.filter(followers__username=user.username)
    context = {
        'profile': profile,
        'topics_followed': topics_followed
    }
    return render(request, 'forum/profile.html', context)


@login_required
def liked_Posts(request):
    user = request.user
    posts = Post.objects.filter(post_pizzas__username__exact=user.username)
    context = {
        'posts': posts
    }
    return render(request, 'forum/liked_Posts_list.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    context = {}
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('forum:profile', username=request.user.username)
        context['error_message'] = form.errors

    form = EditProfileForm(initial={'bio': profile.bio, 'profile_image': profile.profile_image})
    context['form'] = form

    return render(request, 'forum/edit_profile.html', context)


def get_page(page_number, paginator):
    try:
        page_list = paginator.page(page_number)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator(paginator.num_pages)

    return page_list
