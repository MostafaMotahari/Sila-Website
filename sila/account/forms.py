from account.models import Report, User, Referee, Reporter
from league.models import Game, GameImage
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
            "is_referee",
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
        self.referee_object_controler()
        self.reporter_object_controler()

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

    # Check if user is referee
    def referee_object_controler(self):
        # Control referees
        if self.cleaned_data['is_referee'] and not self.instance.is_referee:
            print("referee added")
            Referee.objects.create(user=self.instance)
        
        elif not self.cleaned_data['is_referee'] and self.instance.is_referee:
            print("referee deleted")
            Referee.objects.get(user=self.instance).delete()

    # Check if user is reporter
    def reporter_object_controler(self):
        # Control reporters
        if self.cleaned_data['is_reporter'] and not self.instance.is_reporter:
            print("reporter added")
            Reporter.objects.create(user=self.instance)
        
        elif not self.cleaned_data['is_reporter'] and self.instance.is_reporter:
            print("reporter deleted")
            Reporter.objects.get(user=self.instance).delete()

# A form for creating new users
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

# A form for creating new games
class CreateGameForm(forms.ModelForm):

    # Additional fields
    # Speed imgs of game
    speed_img_one = forms.ImageField(required=False)
    speed_img_one_name = forms.CharField(required=False)
    speed_img_two = forms.ImageField(required=False)
    speed_img_two_name = forms.CharField(required=False)
    speed_img_three = forms.ImageField(required=False)
    speed_img_three_name = forms.CharField(required=False)
    speed_img_four = forms.ImageField(required=False)
    speed_img_four_name = forms.CharField(required=False)

    # Info imgs of game
    info_img_one = forms.ImageField(required=False)
    info_img_one_name = forms.CharField(required=False)
    info_img_two = forms.ImageField(required=False)
    info_img_two_name = forms.CharField(required=False)
    info_img_three = forms.ImageField(required=False)
    info_img_three_name = forms.CharField(required=False)
    info_img_four = forms.ImageField(required=False)
    info_img_four_name = forms.CharField(required=False)

    # Power imgs of game
    power_img_one = forms.ImageField(required=False)
    power_img_one_name = forms.CharField(required=False)
    power_img_two = forms.ImageField(required=False)
    power_img_two_name = forms.CharField(required=False)
    power_img_three = forms.ImageField(required=False)
    power_img_three_name = forms.CharField(required=False)
    power_img_four = forms.ImageField(required=False)
    power_img_four_name = forms.CharField(required=False)

    # Legend imgs of game
    legend_img_one = forms.ImageField(required=False)
    legend_img_one_name = forms.CharField(required=False)
    legend_img_two = forms.ImageField(required=False)
    legend_img_two_name = forms.CharField(required=False)
    legend_img_three = forms.ImageField(required=False)
    legend_img_three_name = forms.CharField(required=False)
    legend_img_four = forms.ImageField(required=False)
    legend_img_four_name = forms.CharField(required=False)

    # Search imgs of game
    search_img_one = forms.ImageField(required=False)
    search_img_one_name = forms.CharField(required=False)
    search_img_two = forms.ImageField(required=False)
    search_img_two_name = forms.CharField(required=False)
    search_img_three = forms.ImageField(required=False)
    search_img_three_name = forms.CharField(required=False)
    search_img_four = forms.ImageField(required=False)
    search_img_four_name = forms.CharField(required=False)

    class Meta:
        model = Game
        fields = [
            "league",
            "home_team",
            "away_team",
            "starts_at",
            "referee",
        ]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateGameForm, self).__init__(*args, **kwargs)

        if not user.is_admin:
            # Disable fields
            self.fields['referee'].disabled = True

