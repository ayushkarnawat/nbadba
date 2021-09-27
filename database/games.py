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
    'http://stats.nba.com/stats/commonallplayers/?',
    headers=HEADERS,
    params={'LeagueID': '00', 'Season': '2015-16', 'IsOnlyCurrentSeason': '0'},
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
    if player[5] == '2016':
        # extract info
        player_id = int(player[0])
        player_name = player[2].replace(u"'",u"")
        team_id = player[10]
        if ((player_id != old_player_id) and (team_id != '')):
            player_game_res = requests.get(
                'http://stats.nba.com/stats/playergamelog/?',
                headers=HEADERS,
                params={
                    'PlayerId': player[0],
                    'LeagueID':'00',
                    'Season':'2015-16',
                    'SeasonType':'Regular Season',
                },
            )
            player_game_data = player_game_res.json()["resultSets"][0]["rowSet"]
            for game in player_game_data:
                game_id = game[2]
                points_scored = game[24]

                # check if this game has already been PUT into database
                query_games = "SELECT * FROM Games WHERE id={}".format(game_id)
                c.execute(query_games)
                game_data = c.fetchone()
                if (game_data == None):
                    game_res = requests.get(
                        'http://stats.nba.com/stats/boxscoresummaryv2/?',
                        headers=HEADERS,
                        params={'GameID': game_id},
                    )
                    game_data = game_res.json()
                    # last_meeting = game_data["resultSets"][6]["rowSet"][0]
                    home_info = game_data["resultSets"][5]["rowSet"][0]
                    away_info = game_data["resultSets"][5]["rowSet"][1]
                    home_team_id = home_info[4]
                    away_team_id = away_info[4]
                    home_points = home_info[22]
                    away_points = away_info[22]
                    game_summary = game_data["resultSets"][0]["rowSet"][0]
                    date = game_summary[0].replace('T',' ')
                    # only one team can win a game (aka no ties)
                    winner = "home" if home_points > away_points else "away"

                    games_query = """
                    INSERT INTO Games(id, date, winning_team,
                                      away_team_id_id, home_team_id_id) \
                    SELECT {4},'{0}','{1}','{2}','{3}'
                    WHERE NOT EXISTS (
                        SELECT *
                        FROM Games
                        WHERE id = {4}
                            OR (away_team_id_id = '{2}'
                            AND home_team_id_id = '{3}'
                            AND date = '{0}'
                        )
                    )
                    """.format(date, winner, away_team_id, home_team_id, game_id)
                    c.execute(games_query)

                    game_score_query = """
                    INSERT INTO GameScore(id, date, home_score, away_score,
                                          away_team_id_id, home_team_id_id)
                    SELECT {5},'{0}',{1},{2},'{3}','{4}'
                    WHERE NOT EXISTS (
                        SELECT *
                        FROM GameScore
                        WHERE id = {5}
                            OR (away_team_id_id = '{3}'
                            AND home_team_id_id = '{4}'
                            AND date = '{0}')
                    )
                    """.format(
                        date,
                        home_points,
                        away_points,
                        away_team_id,
                        home_team_id,
                        game_id,
                    )
                    c.execute(game_score_query)
                else:
                    # get info from game that already exists
                    date = game_data[1]
                    home_team_id = game_data[4]
                    away_team_id = game_data[3]

                plays_in_query = """
                INSERT INTO PlaysIn(id, date, points_scored, player_id_id,
                                    away_team_id_id, home_team_id_id)
                SELECT NULL, '{0}',{1},'{2}','{3}','{4}'
                WHERE NOT EXISTS (
                    SELECT *
                    FROM PlaysIn
                    WHERE away_team_id_id = '{3}'
                        AND home_team_id_id = '{4}'
                        AND date = '{0}'
                        AND player_id_id = '{2}'
                )
                """.format(date, points_scored, player_id, away_team_id,
                        home_team_id)
                c.execute(plays_in_query)
                game_res.close()
            player_game_res.close()
        old_player_id = int(player_id)
conn.commit()
conn.close()
