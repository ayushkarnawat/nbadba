from django import forms
from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn

class PlayersForm(forms.ModelForm):
    player_name = forms.CharField(max_length=30)
    min_height = forms.IntegerField()
    max_height = forms.IntegerField()
    team_name = forms.CharField(max_length=20)
    role = forms.CharField(max_length=20)
    min_points_scored = forms.IntegerField()
    max_points_scored = forms.IntegerField()

    class Meta():
        model = Player
        fields = ['player_name', 'min_height', 'max_height', 'team_name', 'role', 'min_points_scored', 'max_points_scored']
