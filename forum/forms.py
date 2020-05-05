from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Topic, Post
from django.contrib.auth.forms import AuthenticationForm


class LogInForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Please insert a valid email")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'Username', 'id': 'signup_username'}
        self.fields['email'].widget.attrs = {'placeholder': 'Email', 'id': 'signup_email'}
        self.fields['password1'].widget.attrs = {'placeholder': 'Password', 'id': 'signup_password1'}
        self.fields['password2'].widget.attrs = {'placeholder': 'Repeat Password', 'id': 'signup_password2'}

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['slug', 'title', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'video']
