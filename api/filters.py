import django_filters
from league.models import Match, MatchImage, Team


class MatchTimeFilter(django_filters.FilterSet):
    starts_at_ed = django_filters.DateTimeFilter(field_name='starts_at', lookup_expr='date')
    
    class Meta:
        model = Match
        fields = "__all__"