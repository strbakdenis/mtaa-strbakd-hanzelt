from django.shortcuts import render
from backend.mtaa_api.models import Users
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.

def test_user(request):
    user = Users(email_address = 'john.doe@gmail.com', password = 'password', token = 'asdfgh', registration_date='1900-10-10')
    user.save()

    return HttpResponse('asd')

def user_registration(request):
    