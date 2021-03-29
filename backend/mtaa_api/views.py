from django.shortcuts import render
from backend.mtaa_api.models import Users, Cities, Activities, ActivityTypes
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
import random, string
import base64
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


def check_activity_fields(request_body):
    required_fields = ['city', 'activity_type', 'name', 'address', 'thumbnail_description', 'description']

    for field in required_fields:
        if field not in request_body:
            return False
    return True


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
        user = Users(email_address=body['email_address'], password=body['password'], token=random_token,
                     registration_date=timezone.now())
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


@csrf_exempt
def get_cities(request):

    cities = Cities.objects.all()
    array = []
    for city in cities:
        array.append({"id": city.id, "name": city.name})

    return JsonResponse(array, status=200, safe=False)


@csrf_exempt
def get_activities(request):

    city = request.GET.get('city', None)
    activity_type = request.GET.get('activity_type', None)
    array = []

    try:
        activities = Activities.objects.filter(city=city, activity_type=activity_type)
    except Activities.DoesNotExist:
        activities = None
    if activities:

        for activity in activities:
            array.append({"id": activity.id, "name": activity.name,
                          "thumbnail_image": str(activity.thumbnail_image.tobytes()),
                          "thumbnail_description": activity.thumbnail_description})
        return JsonResponse(array, status=200, safe=False)
    else:
        return HttpResponse(status=204)


@csrf_exempt
def get_activity(request):
    activity_id = request.GET.get('id', None)
    response = {}
    try:
        activity = Activities.objects.get(id=activity_id)
    except Activities.DoesNotExist:
        activity = None
    if activity:
        act = {"name": activity.name, "city": activity.city.name, "address": activity.address, "text": activity.description}
        response.update(act)
        return JsonResponse(response, status=200, safe=False)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def add_activity(request):
    
    body = json.loads(request.body)

    token = request.GET.get('token', None)

    if check_activity_fields(body) is False:
        return HttpResponse(status=400)

    try:
        city_object = Cities.objects.get(name=body['city'])
    except Cities.DoesNotExist:
        city_object = None
    if city_object:
        city_number = city_object.id
    else:
        city = Cities(name=body['city'])
        city.save()
        city_object = Cities.objects.get(name=body['city'])
        city_number = city_object.id

    try:
        user_object = Users.objects.filter(token=token)
    except Users.DoesNotExist:
        user_object = None
    if user_object:
        try:
            activity_object = Activities.objects.filter(name=body['name'])
        except Activities.DoesNotExist:
            activity_object = None
        if activity_object:
            return HttpResponse(status=409)
        else:
            activity = Activities(name=body['name'], activity_type=ActivityTypes.objects.get(id=body['activity_type']),
                                  city=Cities.objects.get(id=city_number), address=body['address'],
                                  thumbnail_description=body['thumbnail_description'], description=body['description'])
            activity.save()

            return HttpResponse(status=201)
    else:
        return HttpResponse(status=401)
