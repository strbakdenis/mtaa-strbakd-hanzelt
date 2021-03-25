from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test_user, name='test_user')
]