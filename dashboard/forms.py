from django import forms
from . import models


class PlayersForm(forms.ModelForm):
    player_name = forms.CharField(max_length=30, initial="%")
    min_height = forms.IntegerField(initial=1)
    max_height = forms.IntegerField(initial=100)
    team_name = forms.CharField(max_length=20, initial="%")
    role = forms.CharField(max_length=20, initial="%")
    min_points_scored = forms.IntegerField(initial=1)
    max_points_scored = forms.IntegerField(initial=100)

    class Meta():
        model = models.Player
        fields = [
            "player_name",
            "min_height",
            "max_height",
            "team_name",
            "role",
            "min_points_scored",
            "max_points_scored",
        ]


class HomeAttendeesForm(forms.ModelForm):
    TEAM_CHOICES = (
        ("ATL", "Hawks"),
        ("BKN", "Nets"),
        ("BOS", "Celtics"),
        ("CHA", "Hornets"),
        ("CHI", "Bulls"),
        ("CLE", "Cavaliers"),
        ("DAL", "Mavericks"),
        ("DEN", "Nuggets"),
        ("DET", "Pistons"),
        ("GSW", "Warriors"),
        ("HOU", "Rockets"),
        ("IND", "Pacers"),
        ("LAC", "Clippers"),
        ("LAL", "Lakers"),
        ("MEM", "Grizzlies"),
        ("MIA", "Heat"),
        ("MIL", "Bucks"),
        ("MIN", "Timberwolves"),
        ("NOP", "Pelicans"),
        ("NYK", "Knicks"),
        ("OKC", "Thunder"),
        ("ORL", "Magic"),
        ("PHI", "76ers"),
        ("PHX", "Suns"),
        ("POR", "Trailbrazers"),
        ("SAC", "Kings"),
        ("SAS", "Spurs"),
        ("TOR", "Raptors"),
        ("UTA", "Jazz"),
        ("WAS", "Wizards"),
    )
    team_id = forms.ChoiceField(choices=TEAM_CHOICES)

    class Meta():
        model = models.Team
        fields = ["team_id"]


class WinPercentageForm(forms.ModelForm):
    TEAM_CHOICES = (
        ("ATL", "Hawks"),
        ("BKN", "Nets"),
        ("BOS", "Celtics"),
        ("CHA", "Hornets"),
        ("CHI", "Bulls"),
        ("CLE", "Cavaliers"),
        ("DAL", "Mavericks"),
        ("DEN", "Nuggets"),
        ("DET", "Pistons"),
        ("GSW", "Warriors"),
        ("HOU", "Rockets"),
        ("IND", "Pacers"),
        ("LAC", "Clippers"),
        ("LAL", "Lakers"),
        ("MEM", "Grizzlies"),
        ("MIA", "Heat"),
        ("MIL", "Bucks"),
        ("MIN", "Timberwolves"),
        ("NOP", "Pelicans"),
        ("NYK", "Knicks"),
        ("OKC", "Thunder"),
        ("ORL", "Magic"),
        ("PHI", "76ers"),
        ("PHX", "Suns"),
        ("POR", "Trailbrazers"),
        ("SAC", "Kings"),
        ("SAS", "Spurs"),
        ("TOR", "Raptors"),
        ("UTA", "Jazz"),
        ("WAS", "Wizards"),
    )
    team_id = forms.ChoiceField(choices=TEAM_CHOICES)

    class Meta():
        model = models.Team
        fields = ["team_id"]
