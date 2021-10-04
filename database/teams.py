import json
import requests

import utils


def get_team_info(
    season: str = "2015-16",
    season_type: str = "Regular Season",
    league_id: str = "00",
    use_cached_if_available: bool = True,
    saev: bool = True,
) -> tp.Iterable[tp.Union[str, str, str, str, int, int, int]:
    """Get basic team info for all teams in the specified season."""
    min_year, max_year = utils.parse_years(season)

    res = requests.get("https://stats.nba.com/stats/commonteamyears/?",
                       headers=utils.HEADER,
                       params={"LeagueID": league_id})
    teams = res.json()["resultSets"][0]["rowSet"]
    for team in teams:
        # Only retrieve teams which played in the (specified) season. As the
        # endpoint for commonteamyears returns the min_year (team founded) and
        # max_year (team folded or current year), we check if the specified
        # season is within those years.
        if (int(min_year) >= int(team[2])) and (int(max_year) <= int(team[3])):
            team_id = team[4]
            team_res = requests.get(
                'http://stats.nba.com/stats/teaminfocommon/?',
                headers=HEADERS,
                params={
                    "Season": season,
                    "TeamID": team[1],
                    "LeagueID": league_id,
                    "SeasonType": season_type,
                },
            )
            # detailed team info
            team_info = team_res.json()['resultSets'][0]['rowSet'][0]
            city = team_info[2]
            team_name = team_info[3]
            conference = team_info[5]
            num_wins = team_info[8]
            num_losses = team_info[9]
            rank = team_info[11]
            yield (team_id, city, team_name, conference, num_wins, num_losses,
                    rank,)
