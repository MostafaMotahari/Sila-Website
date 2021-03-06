from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Referee, Reporter, Report, SettingModel

# Admin models
class RefereeAdmin(admin.ModelAdmin):
    list_display = ('user',)

class ReporterAdmin(admin.ModelAdmin):
    list_display = ('user',)

class SettingAdmin(admin.ModelAdmin):
    pass

class ReportAdmin(admin.ModelAdmin):
    list_display = ('writer', 'report_date', 'report_text',)

UserAdmin.fieldsets += (
    ("Custom Fields", {"fields": (
        "is_admin" ,
        "is_captain" ,
        "is_referee" ,
        "is_reporter" ,
        "profile_picture" ,
        "user_telegram_id" ,
        "is_deprived" ,
        "deprived_date" ,
        "deprived_reason" ,
        "is_banned" ,
        "banned_date" ,
        "ban_reason" ,
        "red_cards" ,
        "yellow_cards" ,
        "season_goals" ,
        "played_matchs" ,
        "team" ,
        "trophies" ,
        "total_goals" ,
        "overall_rating" ,
        "player_character" ,
        "admin_level" ,
    )}),
)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Referee, RefereeAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(SettingModel, SettingAdmin)