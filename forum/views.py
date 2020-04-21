from django.shortcuts import render
from .models import Post
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
