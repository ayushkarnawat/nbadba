import json
import requests

import utils


def get_coach_info(
    season: str = "2015-16",
    season_type: str = "Regular Season",
    league_id: str = "00",
    use_cached_if_available: bool = True,
    save: bool = True,
) -> tp.Iterable[tp.Union[str, str, str, str]:
    """Get basic coaches info."""
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
            roster_res = requests.get(
                "http://stats.nba.com/stats/commonteamroster/?",
                headers=utils.HEADER,
                params={
                    "Season": season,
                    "TeamID": team[1],
                    "LeagueID": league_id,
                    "SeasonType": season_type,
                },
            )
            # detailed coach info
            coaches = roster_res.json()["resultSets"][1]["rowSet"]
            for coach in coaches:
                coach_id = coach[2]
                coach_name = coach[5].replace(u"'",u"")
                coach_type = coach[8]
                yield (coach_id, coach_name, coach_type, team_id)
