from django.urls import path
from users import views as user_views
from rest_framework.authtoken import views as drf_token_views

urlpatterns = [
    path('account/', user_views.account),
    path('register/', user_views.register_user),
    path('token/', drf_token_views.obtain_auth_token),
    path('token/refresh/', drf_token_views.obtain_auth_token),
    path('token/revoke/', user_views.revoke_token),
    path('password/change', user_views.change_password),
]
