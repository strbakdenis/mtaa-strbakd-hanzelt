from django.shortcuts import render
from backend.mtaa_api.models import Users
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
import random, string
from django.utils import timezone


def generate_token():
    return(''.join(random.choices(string.ascii_letters + string.digits, k=16)))


def check_email(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex,email)):
        return True

    else:
        return False


def check_required_fields(request_body):
    required_fields = ['password', 'email_address']

    for field in required_fields:
        if field not in request_body:
            return False
    return True


def test_user(request):
    user = Users(email_address = 'john.doe@gmail.com', password = 'qwerty', token = 'asdfgh', registration_date='1900-10-10')
    user.save()

    return HttpResponse('asd')


@csrf_exempt
def user_registration(request):

    body = json.loads(request.body)
    if check_required_fields(body) is False:
        return HttpResponse(status=400)

    if check_email(body['email_address']) is False:
        return HttpResponse(status=400)

    try:
        user_object = Users.objects.filter(email_address=body['email_address'])
    except Users.DoesNotExist:
        user_object = None
    if user_object:
        return HttpResponse(status=409)
    else:
        random_token = generate_token()
        user = Users(email_address=body['email_address'], password=body['password'], token=random_token, registration_date=timezone.now())
        user.save()

    return HttpResponse(status=201)


@csrf_exempt
def user_delete(request):
    token = request.GET.get('token', None)

    if not token:
        return HttpResponse(status=400)

    try:
        user_object = Users.objects.filter(token=token)
    except Users.DoesNotExist:
        user_object = None
    if user_object:
        Users.objects.filter(token=token).delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def user_update(request):

    body = json.loads(request.body)
    token = request.GET.get('token', None)

    if not token:
        return HttpResponse(status=400)

    if check_required_fields(body) is False:
        return HttpResponse(status=400)

    if check_email(body['email_address']) is False:
        return HttpResponse(status=400)

    try:
        user_object = Users.objects.filter(token=token)
    except Users.DoesNotExist:
        user_object = None

    if user_object:
        if Users.objects.filter(email_address=body['email_address']).exists():
            return HttpResponse(status=409)
        Users.objects.filter(token=token).update(email_address=body['email_address'], password=body['password'])
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)


@csrf_exempt
def user_login(request):

    body = json.loads(request.body)

    if check_required_fields(body) is False:
        return HttpResponse(status=400)

    try:
        user_object = Users.objects.get(email_address=body['email_address'], password=body['password'])
    except Users.DoesNotExist:
        user_object = None
    if user_object:
        return JsonResponse({"token": user_object.token}, status=200, safe=False)
    else:
        return HttpResponse(status=404)
