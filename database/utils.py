import typing as tp


HEADER = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/57.0.2987.133 Safari/537.36"
    ),
    "referer": "http://stats.nba.com/scores/",
    "connection": "keep-alive",
}


def parse_years(season: str) -> tp.Union[str, str]:
    # HACK: Check if the season occurs in two different millenium (e.g. the
    # difference between the abbreviated versions of the year is atleast
    # one). For example, for the 1999-00 season, the difference between the
    # abbreviated versions (99 vs. 00) is greater than 1, so we know that
    # this season occurs between millenia.
    min_season_str, max_season_str = season.split("-")
    min_season_two_digit = int(min_season_str[2:])
    max_season_two_digit = int(max_season_str)
    if max_season_two_digit - min_season_two_digit < 0: # case b/t millenium
        max_season_str = str(int(min_season_str[:2]) + 1) + max_season_str
    else:
        max_season_str = min_season_str[:2] + max_season_str
    return min_season_str, max_season_str
