from rest_framework import serializers
from league.models import Match, Team, League

# Serializer for League
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'