from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test_user, name='test_user'),
    path('add', views.user_registration, name='user_registration'),
    path('delete', views.user_delete, name='user_delete'),
    path('update', views.user_update, name='user_update'),
    path('login', views.user_login, name='user_login')
]