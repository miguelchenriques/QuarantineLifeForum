from .models import Post, Topic
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.http.response import JsonResponse


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
