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
res = requests.get(
    "http://stats.nba.com/stats/commonallplayers/?",
    headers=HEADERS,
    params={"LeagueID": "00", "Season": "2015-16", "IsOnlyCurrentSeason": "0"},
)

sqlite_file = "../db.sqlite3"

res_json = res.json()
# with open("players.txt", "rb") as fin:
#     res_json = json.load(fin)
players = res_json["resultSets"][0]["rowSet"]
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

old_player_id = 0
for player in players:
    if player[5] == "2016":
        player_id = int(player[0])
        player_name = player[2].replace(u"'",u"")
        team_id = player[10]
        # only insert players who are (currently) on a team
        if ((player_id != old_player_id) & (team_id != '')):
            player_res = requests.get(
                "http://stats.nba.com/stats/commonplayerinfo/?",
                headers=HEADERS,
                params={"PlayerId": player[0]},
            )
            player_data = players_res.json()["resultSets"][0]["rowSet"]
            height = player_data[0][10]
            position = player_data[0][14]

            query = f"""
            INSERT INTO Players VALUES ('{player_id}', '{player_name}', \
                '{height}', '{team_id}', 'position{}')
            """
            c.execute(query)
            player_res.close()
        old_player_id = int(player_id)
conn.commit()
conn.close()
