from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from league.models import Team, League, Tournament

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

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Tournament, TournamentAdmin)
