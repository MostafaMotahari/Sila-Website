from itertools import count
from django.db import models


# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    level = models.IntegerField(default=1)
    logo = models.ImageField(upload_to='images/league_logos/', blank=True)
    season_number = models.IntegerField(default=1)

    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_teams')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    logo = models.ImageField(upload_to='images/team_logos/', blank=True)
    budget = models.IntegerField(default=0)
    captain = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='captain_of')
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    transfers_in = models.ManyToManyField("account.User", null=True, blank=True, related_name='transferred_in')
    transfers_out = models.ManyToManyField("account.User", null=True, blank=True, related_name='transferred_out')
    due_amount = models.IntegerField(default=0)
    stadium_link = models.URLField(blank=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name


class StadiumModel(models.Model):
    name = models.CharField(max_length=255)
    telegram_chat_id = models.IntegerField(default=0)
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(default=1)


class Transfers(models.Model):
    came_in = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='came_in_transfers')
    came_out = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='came_out_transfers')
    player = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='user_transfers')
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    time_of_expire = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"


class Trophy(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='trophies')
    obtained_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Trophy"
        verbose_name_plural = "Trophies"

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    start_at = models.DateTimeField(auto_now_add=True, null=True)
    end_at = models.DateTimeField(auto_now_add=True, null=True)
    referee = models.ForeignKey("account.Referee", on_delete=models.SET_NULL, null=True, blank=True, related_name='referee_tournaments')
    is_active = models.BooleanField(default=False)
    winner = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='won_tournaments')
    participants = models.ManyToManyField("account.User", null=True, blank=True, related_name='participanted_tournaments')

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True, related_name='tournament_matches')
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True, related_name='league_mathces')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    # home_scores = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='home_goals')
    # away_scores = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='away_goals')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    starts_at = models.DateTimeField(auto_now_add=False, null=True)
    referee = models.ForeignKey("account.Referee", on_delete=models.SET_NULL, null=True, blank=True, related_name="referee_matches")


    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matchs"

    def __str__(self):
        return self.home_team.name + " vs " + self.away_team.name

# Images
class MatchImage(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_images')
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='images/match_pics/')
    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "MatchImage"
        verbose_name_plural = "MatchImages"

    def get_match_details(self):
        return self.match.home_team.name + " vs " + self.match.away_team.name


class Goal(models.Model):
    scorer = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='user_goals')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_goals")
    count = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    def __str__(self):
        return self.scorer.username + " scored at " + str(self.minute) + " minutes"