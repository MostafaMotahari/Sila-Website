from rest_framework import serializers
from league.models import Match, Team, League, MatchImage
from account.models import User

# Serializer for League

# Account serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# League serializers
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class MatchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchImage
        exclude = ["id", "match"]


class MatchSerializer(serializers.ModelSerializer):

    def get_referee(self, obj):
        return {
            "id": obj.referee.user.id,
            "full_name": obj.referee.user.get_full_name(),
            "telegram_id": obj.referee.user.user_telegram_id,
        }

    match_images = MatchImageSerializer(many=True, read_only=True)
    referee = serializers.SerializerMethodField("get_referee")

    class Meta:
        model = Match
        fields = "__all__"
