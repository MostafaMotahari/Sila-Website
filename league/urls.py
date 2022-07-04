from django.urls import path
from league.models import League
from league.views import home, PublicProfileView, TeamProfieView, LeagueTableView

app_name = "league"

urlpatterns = [
    path("", home, name="home"),
    path("profile/<str:username>", PublicProfileView.as_view(), name="public_profile"),
    path("team/<int:pk>", TeamProfieView.as_view(), name="team_profile"),
    path("league/<int:pk>", LeagueTableView.as_view(), name="league_table"),
]