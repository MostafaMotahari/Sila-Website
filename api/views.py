from rest_framework.response import Response
from rest_framework import viewsets
from .filters import MatchTimeFilter, UserByUsernameFilter
from .serializers import (
    MatchSerializer,
    UserSerializer,
    TeamSerializer,
)
from league.models import Match, Team
from account.models import User


# Create your views here.
class MatchAPIView(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_class = MatchTimeFilter


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserByUsernameFilter


class TeamAPIView(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
