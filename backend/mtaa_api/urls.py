from django.urls import path
from . import views

urlpatterns = [
    path('users/test', views.test_user, name='test_user'),
    path('users/add', views.user_registration, name='user_registration'),
    path('users/delete', views.user_delete, name='user_delete'),
    path('users/update', views.user_update, name='user_update'),
    path('users/login', views.user_login, name='user_login'),
    path('cities/', views.get_cities, name='get_cities'),
    path('activities/', views.get_activities, name='get_activities')
]