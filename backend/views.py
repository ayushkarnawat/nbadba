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
            min_height = request.POST['min_height']
            max_height = request.POST['max_height']
            team_name = request.POST['team_name'].lower()
            role = request.POST['role'].lower()
            min_points_scored = request.POST['min_points_scored']
            max_points_scored = request.POST['max_points_scored']

            print("Player: " + player_name)
            print("Min Height: " + min_height)
            print("Max Height: " + max_height)
            print("Team Name: " + team_name)
            print("Role: " + role)
            print("Min Points Scored: " + min_points_scored)
            print("Max Points Scored: " + max_points_scored)

            # Get the list of teams with the associated team name
            team_names = Team.objects.filter(team_name__icontains=team_name)

            # Get average points per game for the list of players with player with the id player
            player_ids = Player.objects.filter(player_name__icontains=player_name)

            avg_points_per_game_for_all_players = []
            for pid in player_ids:
                avg_points_per_game = PlaysIn.objects.filter(player_id=pid).aggregate(Avg('points_scored'))
                avg_points_per_game_for_all_players.append(avg_points_per_game)

            all_players_with_name_height_team_role_points = []
            for team_name in team_names:
                players = Player.objects.filter(player_name__icontains=player_name, height__range=(min_height, max_height), team_name__icontains=team_name, role__icontains=role, points_scored__avg__range=(min_points_scored, max_points_scored))
                all_players_with_name_height_team_role_points.append(players)

            return render(request, 'nba/results.html', {'all_players_with_name_height_team_role_points': all_players_with_name_height_team_role_points})
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
            team = Team.objects.get(team_id = team_id)
            games = Game.objects.filter(home_team_id= team_id)
            for pid in Player:
                for game in games:
                    if(PlaysIn.objects.filter())

<<<<<<< HEAD
                

=======
>>>>>>> 06ec999f54bd30221db50f7397034741ef7c41b0
            return render(request, 'nba/results.html', {'form': form})
        return render(request, 'nba/forms.html', {'form': form})