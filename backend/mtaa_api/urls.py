from django.urls import path
from . import views

urlpatterns = [
    path('users/add', views.user_registration, name='user_registration'),
    path('users/delete', views.user_delete, name='user_delete'),
    path('users/update', views.user_update, name='user_update'),
    path('users/login', views.user_login, name='user_login'),
    path('cities/', views.get_cities, name='get_cities'),
    path('activities/', views.get_activities, name='get_activities'),
    path('activities/activity/', views.get_activity, name='get_activity'),
    path('activities/add/', views.add_activity, name='add_activity')
]