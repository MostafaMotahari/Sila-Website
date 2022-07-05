from rest_framework import serializers
from league.models import Match, Team, League, MatchImage, StadiumModel
from account.models import User

# Serializer for League

# Account serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# Stadium serializer
class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumModel
        exclude = ("team", )

# Filter deprives players
class DeprivingPlayerSerilizer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(is_deprived=False, is_banned=False)
        return super(DeprivingPlayerSerilizer, self).to_representation(data)

# Player serializer
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        list_serializer_class = DeprivingPlayerSerilizer
        fields = ("id", "first_name" ,"last_name" ,"user_telegram_id" ,"is_deprived" ,"deprived_date" ,"is_banned" ,"banned_date")

# League serializers
class TeamSerializer(serializers.ModelSerializer):

    stadium = StadiumSerializer(read_only=True, source='team_stadium')
    players = PlayerSerializer(read_only=True, source="team_players", many=True)
    
    class Meta:
        model = Team
        fields = "__all__"

# Match image serializer
class MatchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchImage
        exclude = ["id", "match"]

# Match serializer
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
