from rest_framework.generics import ListAPIView
from .serializers import MatchSerializer
from league.models import Match

# Create your views here.
class MatchAPIView(ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer