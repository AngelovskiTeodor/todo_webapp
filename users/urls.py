from django.urls import path
from users import views
from rest_framework.authtoken import views as drf_token_views

urlpatterns = [
    path('register/', views.register_user),
    path('token/', drf_token_views.obtain_auth_token),
    path('token/refresh/', drf_token_views.obtain_auth_token),
    #path('token/revoke/', drf_token_views.obtain_auth_token),
]