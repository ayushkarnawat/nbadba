import os
import json
import requests

import utils


def get_game_info(
    season: str = "2015-16",
    season_type: str = "Regular Season",
    league_id: str = "00",
    use_cached_if_available: bool = True,
    save: bool = True,
) -> tp.Iterable[tp.Union[str, str, str, str, int, int, str, str]]:
    """Get games from specified season.

    We first query all players who played in specified season, get the
    games they played in, and retrieve the list of unique games from
    that list.
    """
    min_year, max_year = utils.parse_years(season)

    if use_cached_if_available and os.path.exists("cache/players.json"):
        with open("cache/players.json", "rb") as fin:
            res_json = json.load(fin)
    else:
        print("File not available, querying stats.nba.com...")
        res = requests.get(
            "http://stats.nba.com/stats/commonallplayers/?",
            headers=utils.HEADER,
            params={
                "LeagueID": league_id,
                "Season": season,
                "IsOnlyCurrentSeason": "0",
            },
        )
        res_json = res.json()
        res.close()
        # Save in cache
        if save:
            if not os.path.isdir("cache"):
                os.makedirs("cache")
            with open("cache/players.json", "w") as fout:
                fout.write(res_json)
    players = res_json["resultSets"][0]["rowSet"]

    unique_game_ids = dict()
    for player in players:
        # Only retrieve game info for "active" players who played in the
        # (specified) season. As the endpoint for commonallplayers returns the
        # min_year (rookie) and max_year (player retired or current year), we
        # check if the specified season is within those years.
        if (int(min_year) >= int(player[4])) & (int(max_year) <= int(player[5])):
            team_id = player[10]
            if team_id != "": # is player associated with a team
                player_game_res = requests.get(
                    "http://stats.nba.com/stats/playergamelog/?",
                    headers=utils.HEADER,
                    params={
                        "PlayerId": player[0],
                        "LeagueID": league_id,
                        "Season": season,
                        "SeasonType": season_type,
                    },
                )
                player_game_data = player_game_res.json()["resultSets"][0]["rowSet"]
                player_game_res.close()
                for game in player_game_data:
                    game_id = game[2]
                    # return unique games, as we do not want to (re)insert the
                    # same information multiple times. As we store all
                    # previously queried games in a hashmap (via its unique
                    # game_id), the search is O(1) in the average case.
                    if game_id not in unique_game_ids:
                        unique_game_ids.update({game_id: 1})

                        game_res = requests.get(
                            "http://stats.nba.com/stats/boxscoresummaryv2/?",
                            headers=utils.HEADER,
                            params={"GameID": game_id},
                        )
                        game_data = game_res.json()

                        last_meeting = game_data["resultSets"][6]["rowSet"][0]
                        home_info = game_data["resultSets"][5]["rowSet"][0]
                        away_info = game_data["resultSets"][5]["rowSet"][1]
                        home_team_id = home_info[4]
                        away_team_id = away_info[4]
                        home_points = home_info[22]
                        away_points = away_info[22]
                        game_summary = game_data["resultSets"][0]["rowSet"][0]
                        date = game_summary[0].replace("T"," ").split(" ")[0]
                        # only one team can win a game (aka no ties)
                        winner = "home" if home_points > away_points else "away"
                        yield (game_id, date, away_team_id, home_team_id,
                                away_points, home_points, winner, last_meeting,)


def get_player_specific_game_info(
    season: str = "2015-16",
    season_type: str = "Regular Season",
    league_id: str = "00",
    use_cached_if_available: bool = True,
    save: bool = True,
) -> tp.Iterable[tp.Union[str, str, str, str, int]]:
    """Get all player specific game data from specified season.

    We first query all players who played in the specified season, get
    the games they played in, and then log their game specific info.
    """
    min_year, max_year = utils.parse_years(season)

    if use_cached_if_available and os.path.exists("cache/players.json"):
        with open("cache/players.json", "rb") as fin:
            res_json = json.load(fin)
    else:
        print("File not available, querying stats.nba.com...")
        res = requests.get(
            "http://stats.nba.com/stats/commonallplayers/?",
            headers=utils.HEADER,
            params={
                "LeagueID": league_id,
                "Season": season,
                "IsOnlyCurrentSeason": "0",
            },
        )
        res_json = res.json()
        res.close()
        # Save in cache
        if save:
            if not os.path.isdir("cache"):
                os.makedirs("cache")
            with open("cache/players.json", "w") as fout:
                fout.write(res_json)
    players = res_json["resultSets"][0]["rowSet"]
    for player in players:
        # Only retrieve game info for "active" players who played in the
        # (specified) season. As the endpoint for commonallplayers returns the
        # min_year (rookie) and max_year (player retired or current year), we
        # check if the specified season is within those years.
        if (int(min_year) >= int(player[4])) & (int(max_year) <= int(player[5])):
            player_id = int(player[0])
            team_id = player[10]
            if team_id != "": # is player associated with a team
                player_game_res = requests.get(
                    "http://stats.nba.com/stats/playergamelog/?",
                    headers=utils.HEADER,
                    params={
                        "PlayerId": player[0],
                        "LeagueID": league_id,
                        "Season": season,
                        "SeasonType": season_type,
                    },
                )
                player_game_data = player_game_res.json()["resultSets"][0]["rowSet"]
                player_game_res.close()
                for game in player_game_data:
                    game_id = game[2]
                    points_scored = game[24]

                    # get game specific data; we could obtain a lot more, but
                    # for demonstration purposes this should suffice
                    game_res = requests.get(
                        "http://stats.nba.com/stats/boxscoresummaryv2/?",
                        headers=utils.HEADER,
                        params={"GameID": game_id},
                    )
                    game_data = game_res.json()
                    home_team_id = game_data["resultSets"][5]["rowSet"][0][4]
                    away_team_id = game_data["resultSets"][5]["rowSet"][1][4]
                    game_summary = game_data["resultSets"][0]["rowSet"][0]
                    date = game_summary[0].replace('T',' ')
                    yield (player_id, date, away_team_id, home_team_id,
                            points_scored)
