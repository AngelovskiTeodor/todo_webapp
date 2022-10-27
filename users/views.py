from django.http import JsonResponse
from django.shortcuts import render, redirect
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
@permission_classes([AllowAny])
@api_view(['POST'])
def register_user(request):
    new_user_data = request.data    # JSONParser().parse(request.data)      # Parse request???  koga se koristi @api_view['POST'] ne treba JSONParser
    users_serializer = CreateUserSerializer(data=new_user_data)
    if users_serializer.is_valid():
        users_serializer.save()

        # get token for registered user
        #return token(request)
        #return redirect('/authentication/token/')
        #return get_token(request)       # return the token
    else:
        return JsonResponse(users_serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    user_data = request.data    # JSONParser().parse(request.data)      # Parse request???
    #r = redirect('/authentication/token/')      # ne e vozmozno da se napravi redirect na POST baranje. mora custom da bide
    #r = get_token(request)
    r = Token.objects.get_or_create(user=request.data['username'])
    #r = Response(r.json())     # parse to JSON
    return r


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


# used for oauth
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    r = requests.post(
        'http://0.0.0.0:80/o/revoke_token', data = {
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
    )

    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    else:
        return Response(r.json(), r.status_code)
