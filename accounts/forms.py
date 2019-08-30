from django import forms
from django.contrib.auth.models import User

from fines.models import Player


def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise forms.ValidationError('En användare med det användarnamnet finns redan.', code='invalid')


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError('Användarnamnet med den e-mailadressen finns redan.', code='invalid')


class UserSignupForm(forms.Form):
    first_name = forms.CharField(label='Förnamn', max_length=100)
    last_name = forms.CharField(label='Efternamn', max_length=100)
    email = forms.CharField(label='E-mail', max_length=100)
    username = forms.CharField(label='Användarnamn', max_length=100, validators=[validate_username])
    password = forms.CharField(label='Lösenord', max_length=100, widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Användarnamn', max_length=100)
    password = forms.CharField(label='Lösenord', max_length=100, widget=forms.PasswordInput)
