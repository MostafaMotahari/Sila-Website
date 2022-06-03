from django.urls import path, include
from rest_framework import routers
from .views import MatchAPIView

app_name = 'api'

urlpatterns = [
    path('league/match', MatchAPIView.as_view(), name='match-list'),
]