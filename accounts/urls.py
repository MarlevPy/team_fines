from django.contrib.auth import views
from django.urls import path

from . import views as account_views

urlpatterns = [
    path('login/', account_views.login_user, name='login'),
    path('signup/', account_views.signup, name='signup'),
    path('logout/', account_views.logout_user, name='logout'),
    #path('password_change', views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change_done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('password_reset', views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset_done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]
