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
res = requests.get("http://stats.nba.com/stats/commonteamtears/?",
                 headers=HEADERS,
                 params={"LeagueID": "00"})

sqlite_file = "db.sqlite"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
teams = res.json()['resultSets'][0]['rowSet']
for team in teams:
    if (team[3] == '2016'):
        #TeamID, TeamName, City, rankNum, Conference, num_wins, num_losses
        team_id = team[4]
        team_res = requests.get(
            'http://stats.nba.com/stats/teaminfocommon/?',
            headers=HEADERS,
            params={
                'Season': '2015-16',
                'TeamID': team[1],
                'LeagueID': '00',
                'SeasonType': 'Regular Season',
            },
        )
        # detailed info about team
        team_info = team_res.json()['resultSets'][0]['rowSet'][0]
        team_name = team_info[3]
        city = team_info[2]
        rank = team_info[11]
        conference = team_info[5]
        num_wins = team_info[8]
        num_losses = team_info[9]

        query = "INSERT INTO Teams VALUES ('{}','{}','{}',{},'{}',{},{})".format(
            team_id, team_name, city, rank, conference, num_wins, num_losses
        )
        c.execute(query)
        team_res.close()
conn.commit()
conn.close()
