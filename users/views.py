from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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


# it is never used, because default method provided by DRF is used
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):     # login feature
    user_data = request.data
    username_request = user_data['username']
    password_request = user_data['password']
    user_object = authenticate(username=username_request, password=password_request)
    if user_object:
        user_token = Token.objects.get_or_create(user=username_request)
        print(user_token)
        return user_token
    else:
        try:
            user_object = User.objects.get(username=username_request)
            return JsonResponse({'message': 'Error: Incorrect password'}, status=401)
        except:
            return JsonResponse({'message': 'Error: This user does not exist.'}, status=404)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    request_data=request.data
    username_request = request_data['username']
    current_password_request = request_data['current_password']
    new_password_request = request_data['new_password']
    user_object = authenticate(username=username_request, password=current_password_request)
    if user_object:
        user_object.set_password(new_password_request)
        user_object.save()  # TODO: check if user_object is valid (user_serializer.is_valid())
        user_object.auth_token.delete()
        new_token = Token.objects.get_or_create(user=user_object)[0].key
        response = {'message': 'Password Changed Successfully', 'token': new_token}
        return JsonResponse(response,status=201)
    else:
        return JsonResponse({'message': 'Invalid current password. Please try again'}, status=401)


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

