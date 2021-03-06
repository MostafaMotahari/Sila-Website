from datetime import datetime
from django.shortcuts import render
from django.views.generic import DetailView

from league.models import (
    League,
    Team,
    Match,
    Goal
)
from account.models import (
    User,
    Report,
    SettingModel
)
from account.utilities import iranDateTime

# Create your views here.

# Public profile view
class PublicProfileView(DetailView):
    model = User
    template_name = "league/public_profile.html"

    def get_object(self):
        return User.objects.get(username=self.kwargs.get("username"))

# Team profile view
class TeamProfieView(DetailView):
    model = Team
    template_name = "league/team_profile.html"

# League table view
class LeagueTableView(DetailView):
    model = League
    template_name = "league/league_table.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["ordered_teams"] = context["object"].league_teams.all().order_by("-points")
        return context


# Main page view
def home(request):
    # Finding top scorer of each league and make tables of leagues
    users = User.objects.all().order_by("season_goals")
    leagues = [league for league in League.objects.all()]
    top_scorers = []
    leagues_tables = []

    for user in users:
        if not leagues:
            break

        if user.team:
            if user.team.league:
                if user.team.league in leagues:
                    top_scorers.append(user)
                    leagues_tables.append(Team.objects.filter(league=user.team.league).all().order_by("-points")[:6])
                    leagues.remove(user.team.league)

    # Get three last match results
    last_3_matches = Match.objects.filter(starts_at__lt=iranDateTime(datetime.now())).all().order_by("starts_at")[:3]
    matches_and_goals = {}

    for match in last_3_matches:
        goals = Goal.objects.filter(match=match).all()
        home_team_goals = 0
        away_team_goals = 0

        for goal in goals:
            if goal.scorer in match.home_team:
                home_team_goals += goal.count
            else:
                away_team_goals += goal.count

        matches_and_goals[match] = f"{home_team_goals} - {away_team_goals}"

    # Get top 3 news
    top_3_reports = Report.objects.all().order_by("report_date")[:3]

    # Small details
    players_count = User.objects.all().__len__
    teams_count = Team.objects.all().__len__
    matches_count = Match.objects.all().__len__

    # Fill context data
    context = {
        "settings": SettingModel.objects.first(),
        "top_scorers": top_scorers,
        "leagues_tables": leagues_tables,
        "matches_and_goals": matches_and_goals,
        "top_3_reports": top_3_reports,
        "players_count": players_count,
        "teams_count": teams_count,
        "matches_count": matches_count,
    }
    return render(request, 'league/index.html', context)