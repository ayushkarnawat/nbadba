from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.views.generic import View

from .forms import PlayersForm, HomeAttendeesForm, WinPercentageForm
from .models import Team, Player, GameScore, Game, Coach, Owner, PlaysIn


def index(request):
    teams = Team.objects.all().order_by("team_id")
    players = Player.objects.all()
    games = Game.objects.all()

    template = "backend/index.html"
    context = {
        "page": "index",
        "teams": teams,
        "players": players,
        "games": games,
    }
    return render(request, template, context)


def teams_overview(request):
    teams = Team.objects.all().order_by("team_id")

    template = "backend/teams_overview.html"
    context = {
        "page": "team",
        "teams": teams,
    }
    return render(request, template, context)


def players_overview(request):
    # all players who played during the 2015-16 season
    players = Player.objects.all();

    template = "backend/players_overview.html"
    context = {
        "page": "player",
        "players": players,
    }
    return render(request, template, context)


def games_overview(request):
    # Get all the games from the 2015-16 season
    games = Game.objects.all()

    template = "backend/games_overview.html"
    context = {
        "page": "game",
        "games": games,
    }
    return render(request, template, context)


def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = get_list_or_404(Player, team=team_id)
    coaches = get_list_or_404(Coach, team=team_id)
    owners = get_list_or_404(Owner, team=team_id)

    template = "backend/team_detail.html"
    context = {
        "page": "team",
        "team": team,
        "players": players,
        "coaches": coaches,
        "owners": owners,
    }
    return render(request, template, context)


def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    games_played = get_list_or_404(
        PlaysIn.objects.order_by("date"), player_id=player_id
    )
    avg_points_per_game = PlaysIn.objects.filter(
        player_id=player_id).aggregate(Avg("points_scored"))

    template = "backend/player_detail.html"
    context = {
        "page": "player",
        "player": player,
        "games_played": games_played,
        "avg_points_per_game": avg_points_per_game,
    }
    return render(request, template, context)


def game_detail(request, year, month, day, away_team_id, home_team_id):
    """Retrieve specific details about a certain game."""
    # get game with the same date, home team, and away team
    date = year + "-" + month + "-" + day
    game = get_object_or_404(
        Game,
        date=date,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )
    game_score = get_object_or_404(
        GameScore,
        date=date,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )
    players_who_played_in_game = get_list_or_404(
        PlaysIn.objects.order_by("points_scored"),
        date=date,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )

    template = "backend/game_detail.html"
    context = {
        "page": "game",
        "game": game,
        "game_score": game_score,
        "players_who_played_in_game": players_who_played_in_game,
    }
    return render(request, template, context)


class PlayersFormView(View):
    form_class = PlayersForm

    def get(self, request):
        form = self.form_class(None)
        template = "backend/players_query.html"
        context = {"page": "player_query", "form": form}
        return render(request, template, context)

    def post(self, request):
        if request.method == "POST":
            player_name = request.POST["player_name"].lower()
            min_height = int(request.POST["min_height"])
            max_height = int(request.POST["max_height"])
            team_name = request.POST["team_name"].lower()
            role = request.POST["role"].lower()
            min_points_scored = int(request.POST["min_points_scored"])
            max_points_scored = int(request.POST["max_points_scored"])

            query = """
            SELECT Player_Name, Team_name, Role, Height, avg(Points_Scored) as avg, Player_ID
            FROM Players p, PlaysIn, Teams t
            WHERE Player_ID = Player_ID_ID
                AND player_Name like '%%{}%%'
                AND height > {}
                AND height < {}
                AND Team_Name like '%%{}%%'
                AND p.team_id = t.team_id
                AND p.role like '%%{}%%'
            GROUP BY Player_ID
            Having avg(Points_Scored) > {} and avg(Points_Scored) < {}
            """.format(
                player_name,
                min_height,
                max_height,
                team_name,
                role,
                min_points_scored,
                max_points_scored,
            )

            players = Player.objects.raw(query)

            template = "backend/results.html"
            context = {"page": "player_query", "players": players}
            return render(request, template, context)

        form = self.form_class(request.POST)
        template = "backend/forms.html"
        context = {"page": "player_query", "form": form}
        return render(request, template, context)


class HomeAttendeesFormView(View):
    form_class = HomeAttendeesForm

    def get(self, request):
        form = self.form_class(None)
        template = "backend/teams_query.html"
        context = {"page": "team_query", "form": form}
        return render(request, template, context)

    def post(self, request):
        if request.method == "POST":
            team_id = request.POST['team_id']
            query = """
            SELECT p.Player_name, p.player_id
            FROM Players p
            WHERE NOT EXISTS (SELECT *
                    FROM games g
                    WHERE g.home_team_id_id = '{}'
                    AND NOT EXISTS (SELECT *
                        FROM playsIn pi
                        WHERE g.away_team_id_id = pi.away_team_id_id
                            AND g.home_team_id_id = pi.home_team_id_id
                            AND g.date = pi.date
                            AND p.player_id = pi.player_id_id))
            """.format(team_id)

            players = Player.objects.raw(query)

            template = "backend/results2.html"
            context = {"page": "team_query", "players": players}
            return render(request, template, context)

        form = self.form_class(request.POST)
        template = "backend/forms.html"
        context = {"page": "team_query", "form": form}
        return render(request, template, context)


class WinPercentageFormView(View):
    form_class = WinPercentageForm

    def get(self, request):
        form = self.form_class(None)
        template = "backend/win_percentage_query.html"
        context = {"page": "win_query", "form": form}
        return render(request, template, context)

    def post(self, request):
        if request.method == "POST":
            team_id = request.POST["team_id"]
            print(team_id)

            query = """
            SELECT t.team_Name, t.team_id, (count(*) / 41.) AS cnt
            FROM Games g, Teams t
            WHERE t.team_ID = g.home_Team_ID_id
                AND g.winning_Team like 'home'
                AND t.team_ID = '{}'
            """.format(team_id)
            teams = Team.objects.raw(query)
            template = "backend/results3.html"
            context = {"page": "win_query", "teams": teams}
            return render(request, template, context)

        form = self.form_class(request.POST)
        template = "backend/forms.html"
        context = {"page": "win_query", "form": form}
        return render(request, template, context)
