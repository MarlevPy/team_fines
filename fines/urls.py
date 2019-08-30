from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fines', views.fines_index, name='fines_index'),
    path('<int:pk>/', views.player_detail, name='player_detail'),
    path('high_score', views.high_score, name='high_score'),
    path('new_fine', views.new_fine, name='new_fine'),
    path('remove_fine/<int:pk>/', views.remove_fine, name='remove_fine'),
    path('register_payment', views.register_payment, name='register_payment'),
    path('remove_payment/<int:pk>/', views.remove_payment, name='remove_payment'),
]
