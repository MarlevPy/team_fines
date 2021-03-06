from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:pk>/', views.player_detail, name='player_detail'),
    path('high_score', views.high_score, name='high_score'),
    path('fines_list', views.fines_list, name='fines_list'),
    path('players_list', views.players_list, name='players_list'),
    path('new_fine', views.new_fine, name='new_fine'),
    path('remove_fine/<int:pk>/', views.remove_fine, name='remove_fine'),
    path('register_payment', views.register_payment, name='register_payment'),
    path('remove_payment/<int:pk>/', views.remove_payment, name='remove_payment'),
    path('register_sponsoring', views.register_sponsoring, name='register_sponsoring'),
    path('remove_sponsor/<int:pk>/', views.remove_sponsor, name='remove_sponsor'),
]
