import django_filters
from league.models import Match
from account.models import User


class MatchTimeFilter(django_filters.FilterSet):
    starts_at_ed = django_filters.DateTimeFilter(field_name='starts_at', lookup_expr='date')
    
    class Meta:
        model = Match
        fields = "__all__"


class UserByUsernameFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user_telegram_id')

    class Meta:
        model = User
        exclude = ("profile_picture", )