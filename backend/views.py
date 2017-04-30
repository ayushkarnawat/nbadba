# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View

from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn

# Create your views here.
def index(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    games = Game.objects.all()
    return render(request, 'nba/index.html', {'teams': teams, 'players': players, 'games': games})

def teams_overview(request):
    teams = Team.objects.all()
    return render(request, 'nba/teams_overview.html', {'teams': teams})

def players_overview(request):
    players = Player.objects.all();
    return render(request, 'nba/players_overview.html', {'players': players})

def games_overview(request):
    games = Game.objects.all()
    return render(request, 'nba/games_overview.html', {'games': games})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # queryset = Player.objects.filter(team__startswith = '')
    players = get_list_or_404(Player, team=team_id)
    # coaches = get_list_or_404(Coach, team=team_id)
    # owners = get_list_or_404(Owner, team=team_id)
    return render(request, 'nba/team_detail.html', {'team': team, 'players': players})

def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, 'nba/player_detail.html', {'player': player})

def game_detail(request, year, month, day, away_team_id, home_team_id):
    date = year + "-" + month + "-" + day

    # Get the game with the same date, home team, and away team
    game = get_object_or_404(Game, date=date, home_team_id=home_team_id, away_team_id=away_team_id)
    game_score = get_object_or_404(GameScore, date=date, home_team_id=home_team_id, away_team_id=away_team_id)

    # Get all players who played in this specific game
    players_who_played_in_game = get_list_or_404(PlaysIn, date=date, home_team_id=home_team_id, away_team_id=away_team_id)
    return render(request, 'nba/game_detail.html', {'game': game, 'game_score': game_score, 'players_who_played_in_game': players_who_played_in_game})