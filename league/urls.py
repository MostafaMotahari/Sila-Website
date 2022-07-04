from django.urls import path
from league.views import home, PublicProfileView, TeamProfieView

app_name = "league"

urlpatterns = [
    path("", home, name="home"),
    path("profile/<int:pk>", PublicProfileView.as_view(), name="public_profile"),
    path("team/<int:pk>", TeamProfieView.as_view(), name="team_profile"),
]