from django.contrib.auth import views
from django.urls import path

from . import views as account_views

urlpatterns = [
    path('login/', account_views.login_user, name='login'),
    path('signup/', account_views.signup, name='signup'),
    path('logout/', account_views.logout_user, name='logout'),
]
