from django.shortcuts import render
import league

from league.models import (
    League,
    Team
)
from account.models import (
    User
)

# Create your views here.
def home(request):
    # Finding top scorer of each league
    users = User.objects.all().order_by("season_goals")
    leagues = [league for league in League.objects.all()]
    top_scorers = []

    for user in users:
        if not leagues:
            break

        if user.team.league in leagues:
            top_scorers.append(user)
            leagues.remove(user.team.league)

    context = {
        "top_scorers": top_scorers,
    }
    return render(request, 'league/index.html', context)