# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.db.models import Count, Avg

from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn
from .forms import PlayersForm, HomeAttendeesForm

# Create your views here.
def index(request):
    # Get all the teams, players, and games
    teams = Team.objects.all().order_by('team_id')
    players = Player.objects.all()
    games = Game.objects.all()
    return render(request, 'nba/index.html', {'teams': teams, 'players': players, 'games': games})

def teams_overview(request):
    # Get all the teams in the NBA
    teams = Team.objects.all().order_by('team_id')
    return render(request, 'nba/teams_overview.html', {'teams': teams})

def players_overview(request):
    # Get all the players who played in the NBA in 2015-16 season
    players = Player.objects.all();
    return render(request, 'nba/players_overview.html', {'players': players})

def games_overview(request):
    # Get all the games from the 2015-16 season
    games = Game.objects.all()
    return render(request, 'nba/games_overview.html', {'games': games})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = get_list_or_404(Player, team=team_id)
    coaches = get_list_or_404(Coach, team=team_id)
    owners = get_list_or_404(Owner, team=team_id)
    return render(request, 'nba/team_detail.html', {'team': team, 'players': players, 'coaches': coaches,  'owners': owners})

def player_detail(request, player_id):
    # Get the specific player
    player = get_object_or_404(Player, pk=player_id)

    # Get all the games the player played in
    games_played = get_list_or_404(PlaysIn.objects.order_by('date'), player_id=player_id)

    # Get the average points per game for the season for the player
    avg_points_per_game = PlaysIn.objects.filter(player_id=player_id).aggregate(Avg('points_scored'))
    return render(request, 'nba/player_detail.html', {'player': player, 'games_played': games_played, 'avg_points_per_game': avg_points_per_game})

def game_detail(request, year, month, day, away_team_id, home_team_id):
    """
    Gives specific details about a certain game_detail

    Params:
    -------
        year: (int 4)
            The year when the game took place

        month: (int 2)
            The month when the game took place

        day: (int 2)
            The day when the game took place

        away_team_id: (char 3)
            Unique team id of the away team

        home_team_id: (char 3)
            Unique team id of the home team
    
    Returns:
    --------
        render: (HTTP Request, HTML Template)
            A HTTP page with the dynamic information filled in 
    """
    # Get the game with the same date, home team, and away team
    date = year + "-" + month + "-" + day
    game = get_object_or_404(Game, date=date, home_team_id=home_team_id, away_team_id=away_team_id)
    game_score = get_object_or_404(GameScore, date=date, home_team_id=home_team_id, away_team_id=away_team_id)

    # Get all players who played in this specific game
    players_who_played_in_game = get_list_or_404(PlaysIn.objects.order_by('points_scored'), date=date, home_team_id=home_team_id, away_team_id=away_team_id)
    return render(request, 'nba/game_detail.html', {'game': game, 'game_score': game_score, 'players_who_played_in_game': players_who_played_in_game})

class PlayersFormView(View):
    form_class = PlayersForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'nba/players_query.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if request.method == "POST":
            player_name = request.POST['player_name'].lower()
            min_height = int(request.POST['min_height'])
            max_height = int(request.POST['max_height'])
            team_name = request.POST['team_name'].lower()
            role = request.POST['role'].lower()
            min_points_scored = int(request.POST['min_points_scored'])
            max_points_scored = int(request.POST['max_points_scored'])

            query = """SELECT Player_Name, Team_name, Role, Height, avg(Points_Scored) as avg, Player_ID
                        FROM Players p, PlaysIn, Teams t
                        WHERE Player_ID = Player_ID_ID
                            AND player_Name like '%%{}%%'
                            AND height > {}
                            AND height < {}
                            AND Team_Name like '%%{}%%'
                            AND p.team_id = t.team_id
                            AND p.role like '%%{}%%'
                        GROUP BY Player_ID
                        Having avg(Points_Scored) > {} and avg(Points_Scored) < {}""".format(player_name, min_height, max_height, team_name, role, min_points_scored, max_points_scored)

            players = Player.objects.raw(query)

            return render(request, 'nba/results.html', {'players': players})
        return render(request, 'nba/forms.html', {'form': form})

class HomeAttendeesFormView(View):
    form_class = HomeAttendeesForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'nba/teams_query.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if request.method == "POST":
            team_id = request.POST['team_id']
            print(team_id)
            query = """SELECT p.Player_name, p.player_id
                        FROM Players p
                        WHERE NOT EXISTS (SELECT *
                                FROM games g
                                WHERE g.home_team_id_id = '%%{}%%'
                                AND NOT EXISTS (SELECT *	
                                    FROM playsIn pi
                                    WHERE g.away_team_id_id = pi.away_team_id_id
                                        AND g.home_team_id_id = pi.home_team_id_id
                                        AND g.date = pi.date
                                        AND p.player_id = pi.player_id_id))""".format(team_id)

            all_players = Player.objects.raw(query)                         
            return render(request, 'nba/results2.html', {'all_players': all_players})
        return render(request, 'nba/forms.html', {'form': form})