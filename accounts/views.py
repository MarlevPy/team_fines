from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .forms import UserLoginForm, UserSignupForm
from fines.models import Player
from fines.views import logger


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f'User login: {user}')
                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    logger.info(f'User logout: {request.user}')
    return render(request, 'logout.html')


def signup(request):
    form = UserSignupForm(request.POST or None)
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            player = get_player(first_name, last_name)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            if player:
                user.player.set(player)
            else:
                logger.error(f'User created without setting player: {user}')

            user = authenticate(username=username, password=password)
            login(request, user)
            logger.info(f'User created and player was set: {user}')
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'signup.html', {'form': form})


def get_player(first_name, last_name):
    return Player.objects.filter(first_name=first_name.capitalize(), last_name=last_name.capitalize())
