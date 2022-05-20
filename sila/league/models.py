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


class Team(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    logo = models.ImageField(upload_to='images/team_logos/', blank=True)
    budget = models.IntegerField(default=0)
    captain = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='captain')
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    transfers_in = models.ManyToManyField("account.User", null=True, blank=True, related_name='transfers_in')
    transfers_out = models.ManyToManyField("account.User", null=True, blank=True, related_name='transfers_out')
    due_amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Transfers(models.Model):
    came_in = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='came_in')
    came_out = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='came_out')
    player = models.ForeignKey("account.User", on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    time_of_expire = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"


class Trophy(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    obtained_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Trophy"
        verbose_name_plural = "Trophies"


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    start_at = models.DateTimeField(auto_now_add=True, null=True)
    end_at = models.DateTimeField(auto_now_add=True, null=True)
    refree = models.OneToOneField("account.Refree", on_delete=models.SET_NULL, null=True, blank=True, related_name='refree')
    is_active = models.BooleanField(default=False)
    winner = models.OneToOneField("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')
    participants = models.ManyToManyField("account.User", null=True, blank=True, related_name='participants')

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"


class Game(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    league = models.OneToOneField(League, on_delete=models.CASCADE, null=True, blank=True)
    home_team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='home')
    away_team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='away')
    home_scores = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='home_scores')
    away_scores = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='away_scores')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    starts_at = models.DateTimeField(auto_now_add=False, null=True)
    refree = models.OneToOneField("account.Refree", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"