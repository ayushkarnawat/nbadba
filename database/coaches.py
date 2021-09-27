import json
import sqlite3
import requests


HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/57.0.2987.133 Safari/537.36"
    ),
    "referer": "http://stats.nba.com/scores/",
    "connection": "keep-alive",
}
res = requests.get("https://stats.nba.com/stats/commonteamyears/?",
                   headers=HEADERS,
                   params={"LeagueID": "00"})

sqlite_file = "db.sqlite3"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
teams = res.json()["resultSets"][0]["rowSet"] # teams and ids
for team in teams:
    if team[3] == "2016":
        # coach_id, coach_name, coach_type, team_id
        team_id = team[4]
        roster_res = requests.get(
            "http://stats.nba.com/stats/commonteamroster/?",
            headers=HEADERS,
            params={
                "Season": "2015-16",
                "TeamID": team[1],
                "LeagueID": "00",
                "SeasonType": "Regular Season",
            },
        )
        # detailed team info
        fullContent = roster_res.json()
        coaches = fullContent["resultSets"][1]["rowSet"]
        for coach in coaches:
            coach_id = coach[2]
            coach_name = coach[5].replace(u"'",u"")
            coach_type = coach[8]
            query = """
            INSERT INTO Coaches
            SELECT '{1}','{3}','{2}','{0}'
            WHERE NOT EXISTS (
                SELECT *
                FROM Coaches
                WHERE coach_id = '{0}'
            )
            """.format(coach_id, coach_name, coach_type, team_id)
            c.execute(query)
        roster_res.close()
conn.commit()
conn.close()
res.close()
