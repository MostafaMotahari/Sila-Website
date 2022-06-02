from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    is_captain = models.BooleanField(default=False, verbose_name="Captain")
    is_referee = models.BooleanField(default=False, verbose_name="Referee")
    is_reporter = models.BooleanField(default=False, verbose_name="Reporter")
    profile_picture = models.ImageField(upload_to='images/profile_pictures/', blank=True, verbose_name="Profile Picture")
    user_telegram_id = models.CharField(max_length=100, blank=True, verbose_name="Telegram ID")
    email = models.EmailField(max_length=100, blank=True, verbose_name="Email")
    is_deprived = models.BooleanField(default=False, verbose_name="Deprived")
    deprived_date = models.DateTimeField(blank=True, null=True, verbose_name="Deprived Date")
    deprived_reason = models.TextField(blank=True, verbose_name="Deprived Reason")
    is_banned = models.BooleanField(default=False, verbose_name="Banned")
    banned_date = models.DateTimeField(blank=True, null=True, verbose_name="Banned Date")
    ban_reason = models.TextField(blank=True, verbose_name="Ban Reason")
    red_cards = models.IntegerField(default=0, verbose_name="Red Cards")
    yellow_cards = models.IntegerField(default=0, verbose_name="Yellow Cards")
    season_goals = models.IntegerField(default=0, verbose_name="Goals")
    played_matchs = models.IntegerField(default=0, verbose_name="Played Matchs")
    team = models.ForeignKey("league.Team", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Team", related_name="team_players")
    trophies = models.ManyToManyField("league.Trophy", blank=True, verbose_name="Trophies")
    total_goals = models.IntegerField(default=0, verbose_name="Total Goals")
    overall_rating = models.IntegerField(default=0, verbose_name="Overall Rating")
    player_character = models.CharField(max_length=100, blank=True, verbose_name="Player Character")

    # Admin level
    amdin_levels = (
        (0, "None"),
        (1, "Top-Level"),
        (2, "Midd-Level"),
    )

    admin_level = models.IntegerField(choices=amdin_levels, default=2, verbose_name="Admin Level")


    def get_absolute_url(self):
        return reverse("account:profile")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Referee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="referee_user")
    level = models.IntegerField(default=0, verbose_name="Level")
    experience = models.IntegerField(default=0, verbose_name="Experience")
    level_up_date = models.DateTimeField(blank=True, null=True, verbose_name="Level Up Date")

    class Meta:
        verbose_name = "Referee"
        verbose_name_plural = "Referees"

    def __str__(self):
        return self.user.get_full_name()


class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="reporter_user")
    level = models.IntegerField(default=0, verbose_name="Level")
    experience = models.IntegerField(default=0, verbose_name="Experience")
    level_up_date = models.DateTimeField(blank=True, null=True, verbose_name="Level Up Date")

    class Meta:
        verbose_name = "Reporter"
        verbose_name_plural = "Reporters"

    def __str__(self):
        return self.user.get_full_name()


class Report(models.Model):
    report_date = models.DateTimeField(blank=True, null=True, verbose_name="Report Date")
    report_text = models.TextField(blank=True, verbose_name="Report Text")
    reporter_object = models.ForeignKey(Reporter, on_delete=models.CASCADE, blank=True, null=True, verbose_name="reports")

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"