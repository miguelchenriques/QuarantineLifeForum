from django.shortcuts import render
from .models import Post, Topic, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

page_size = 10


# Forum display Views
def homepage(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, page_size)
    page_number = request.GET.get('page', 1)

    page_list = get_page(page_number, paginator)

    context = {
        'page_list': page_list,
    }
    return render(request, 'forum/index.html', context)


def topic_details(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    context = {
        'topic': topic
    }
    # return render(request, 'forum/topic_details.html', context)
    return None


def post_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post
    }
    # return render(request, 'forum/post_details.html', context)
    return None


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


# Similar code in pagination
def get_page(page_number, paginator):
    try:
        page_list = paginator.page(page_number)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator(paginator.num_pages)

    return page_list


# Authentication Views

