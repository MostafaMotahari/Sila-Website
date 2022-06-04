from ast import MatchValue
from django.urls import path, include
from rest_framework import routers
from .views import (
    MatchAPIView,
    UserAPIView,
    TeamAPIView,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

router = routers.SimpleRouter()
router.register('matches', MatchAPIView, basename='matches')
router.register('teams', TeamAPIView, basename='teams')
router.register('users', UserAPIView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', obtain_auth_token),
]