from django.db.models import Count
from .forms import LogInForm, UserSignUpForm
from .models import Topic


def accounts_form_context(request):
    context = {
        'loginForm': LogInForm(),
        'signupForm': UserSignUpForm()
    }
    return context


def top_topics_context(request):
    context = {
        'topTopics': Topic.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')[:10]
    }
    return context
