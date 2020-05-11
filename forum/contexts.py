from django.db.models import Count
from .forms import LogInForm, UserSignUpForm
from .models import Topic
from .views import MINIMUM_REPUTATION_TO_CREATE_TOPIC


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


def create_topic_reputation_context(request):
    context = {
        'minTopicRep': MINIMUM_REPUTATION_TO_CREATE_TOPIC
    }
    return context
