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

class HomeAttendeesForm(forms.ModelForm):
    TEAM_CHOICES = (
        ('Hawks', 'ATL'),
        ('Nets', 'BKN'),
        ('Celtics', 'BOS'),
        ('Hornets', 'CHA'),
        ('Bulls', 'CHI'),
        ('Cavaliers', 'CLE'),
        ('Mavericks', 'DAL'),
        ('Nuggets', 'DEN'),
        ('Pistons', 'DET'),
        ('Warriors', 'GSW'),
        ('Rockets', 'HOU'),
        ('Pacers', 'IND'),
        ('Clippers', 'LAC'),
        ('Lakers', 'LAL'),
        ('Grizzlies', 'MEM'),
        ('Heat', 'MIA'),
        ('Bucks', 'MIL'),
        ('Timberwolves', 'MIN'),
        ('Pelicans', 'NOP'),
        ('Knicks', 'NYK'),
        ('Thunder', 'OKC'),
        ('Magic', 'ORL'),
        ('76ers', 'PHI'),
        ('Suns', 'PHX'),
        ('Trailbrazers', 'POR'),
        ('Kings', 'SAC'),
        ('Spurs', 'SAS'),
        ('Raptors', 'TOR'),
        ('Jazz', 'UTA'),
        ('Wizards', 'WAS'),
    )
    team_id = forms.ChoiceField(choices=TEAM_CHOICES)
    
    class Meta():
        model = Team
        fields = ['team_id']