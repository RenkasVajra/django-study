from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SiteUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = SiteUser
        fields = ('username', 'password')
