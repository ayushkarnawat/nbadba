# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View, UpdateView, ListView # added UpdateView + ListView
from django.http import HttpResponse, HttpResponseRedirect

from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn

# Create your views here.
def index(request):
    teams = Team.objects.all();
    players = Player.objects.all();
    games = Game.objects.all();
    return render(request, 'nba/index.html', {'teams': teams, 'players': players, 'games': games})

def teams_overview(request):
    teams = Team.objects.all();
    return render(request, 'nba/teams_overview.html', {'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, 'nba/team_detail.html', {'team': team})

def players_overview(request):
    players = Player.objects.all();
    return render(request, 'nba/players_overview.html', {'players': players})