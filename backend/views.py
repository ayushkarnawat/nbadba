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
    # owners = get_object_or_404(Owner, team=team_id)
    return render(request, 'nba/team_detail.html', {'team': team, 'players': players})

def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, 'nba/player_detail.html', {'player': player})