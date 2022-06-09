from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from league.models import Team, League, Tournament, Match, MatchImage

# Admin models
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('-created_at',)

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'level', 'season_number')
    list_filter = ('level',)
    search_fields = ('name',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'captain', 'budget', 'points', 'due_amount')
    list_filter = ('league',)
    search_fields = ('name',)

class MatchAdmin(admin.ModelAdmin):
    list_display = ("league", "home_team", "away_team", "created_at", "starts_at", "referee", )
    ordering = ('-starts_at', )
    search_fields = ('team1', 'team2')

class MatchImageAdmin(admin.ModelAdmin):
    list_display = ("get_match_details", "name", "type", )
    ordering = ('-pk', )

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchImage, MatchImageAdmin)
