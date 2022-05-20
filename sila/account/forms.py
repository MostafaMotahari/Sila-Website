from account.models import User
from django import forms
import datetime

# Forms
class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            # "is_active",
            "is_admin",
            # "amdin_level", # Add this field later to html template and set their permissions
            "is_captain",
            "is_refree",
            "is_reporter",
            "profile_picture",
            "user_telegram_id",
            "email",
            "is_deprived",
            "deprived_date",
            "deprived_reason",
            "is_banned",
            "banned_date",
            "ban_reason",
            "red_cards",
            "yellow_cards",
            "season_goals",
            "played_games",
            "team",
            # "trophies",
            "total_goals",
            # "overall_rating",
            "player_character",
        ]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['is_banned'].disabled = True
            self.fields['banned_date'].disabled = True
            self.fields['ban_reason'].disabled = True
            self.fields['player_character'].disabled = True
            self.fields['is_captain'].disabled = True
            # self.fields['trophies'].disabled = True
            self.fields['is_admin'].disabled = True
            self.fields['total_goals'].disabled = True


    def clean(self):
        cleaned_data = super(UpdateUserForm, self).clean()

        # Apply football rules
        self.football_rules_controler()

        return cleaned_data


    # Football rules controler
    def football_rules_controler(self):

        # Control goals
        if self.instance.total_goals == 0:
            self.cleaned_data['total_goals'] = self.cleaned_data['season_goals']
        else:
            self.cleaned_data['total_goals'] = (self.instance.total_goals - self.instance.season_goals) + int(self.cleaned_data['season_goals'])

        # Control yellow cards and depriving
        if int(self.cleaned_data['yellow_cards']) % 5 == 0 and int(self.cleaned_data['yellow_cards']) != 0:
            # Deprive user
            self.cleaned_data['is_deprived'] = True
            self.cleaned_data['deprived_date'] = datetime.datetime.now() + datetime.timedelta(days=1)
            self.cleaned_data['deprived_reason'] = 'Red cards'

        # Control red cards and depriving
        elif int(self.cleaned_data['red_cards']) > self.instance.red_cards:
            # Deprive user
            self.cleaned_data['is_deprived'] = True
            self.cleaned_data['deprived_date'] = datetime.datetime.now() + datetime.timedelta(days=1)
            self.cleaned_data['deprived_reason'] = 'Red cards'


class CreateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "is_active",
            "is_admin",
            "admin_level", # Add this field later to html template and set their permissions
            "profile_picture",
            "user_telegram_id",
            "email",
            "overall_rating",
            "player_character",
        ]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateUserForm, self).__init__(*args, **kwargs)

        if user.admin_level == 1:
            # Disable fields
            self.fields['is_active'].disabled = True
            self.fields['is_admin'].disabled = True
            self.fields['admin_level'].disabled = True