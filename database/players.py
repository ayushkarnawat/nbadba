import os
import json
import requests

import utils


def get_player_info(
    season: str = "2015-16",
    league_id: str = "00",
    use_cached_if_available: bool = True,
    save: bool = True,
) -> tp.Iterable[tp.Union[str, str, str, str, str]]:
    """Get basic player info."""
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
                "IsOnlyCurrentSeason": '0',
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
        # Only retrieve player info for "active" players who played in the
        # (specified) season. As the endpoint for commonallplayers returns the
        # min_year (rookie) and max_year (player retired or current year), we
        # check if the specified season is within those years.
        if (int(min_year) >= int(player[4])) & (int(max_year) <= int(player[5])):
            player_id = int(player[0])
            player_name = player[2].replace(u"'",u"")
            team_id = player[10]
            if team_id != "": # is player associated with a team
                player_res = requests.get(
                    "http://stats.nba.com/stats/commonplayerinfo/?",
                    headers=utils.HEADER,
                    params={"PlayerId": player[0]},
                )
                player_data = players_res.json()["resultSets"][0]["rowSet"]
                height = player_data[0][10]
                position = player_data[0][14]
                yield (player_id, player_name, height, team_id, position,)
