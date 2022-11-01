from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token as get_token
from rest_framework.authtoken.models import Token
import requests
import environ

from users.serializers import CreateUserSerializer

env = environ.Env()
# reading .env file
environ.Env.read_env()
CLIENT_ID = env('OAUTH_CLIENT_ID')
CLIENT_SECRET = env('OAUTH_CLIENT_SECRET')


@csrf_exempt
#@permission_classes([AllowAny])
@api_view(['POST'])
def register_user(request):
    new_user_data = request.data
    users_serializer = CreateUserSerializer(data=new_user_data)
    if users_serializer.is_valid():
        created_user = users_serializer.save()
        response_data = {}
        token = Token.objects.get_or_create(user=created_user)[0].key
        response_data['message'] = 'Registration successful'
        response_data['username'] = users_serializer.data['username']
        response_data['token'] = token
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse(users_serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    user_data = request.data
    username_request = user_data['username']
    password_request = user_data['password']
    user_object = User.objects.get(username=username_request)   # throwns User.DoesNotExist exception
    if password_request == user_object.password:
        user_token = Token.objects.get_or_create(user=username_request)
        return user_token
    else:
        return JsonResponse({'message': 'Error: This user does not exist'}, status=404)


# used for oauth
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    r = requests.post(
        'http://0.0.0.0:80/o/token/', data = {
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
    )
    return Response(r.json())


@csrf_exempt
@api_view(['GET'])#, 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([AllowAny])
def revoke_token(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        return JsonResponse({'message': 'Logout Unsuccessful'}, status=404)
    return JsonResponse({'message': 'Logout Successful'}, status=201)

