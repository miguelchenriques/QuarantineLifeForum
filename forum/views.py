from django.shortcuts import render
from .models import Post, Topic, Comment
from django.core.paginator import Paginator


# Create your views here.
def homepage(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET['page']
    page_list = paginator.get_page(page_number)
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
