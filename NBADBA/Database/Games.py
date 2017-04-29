import requests
import json

import sqlite3
HEADERS = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/57.0.2987.133 Safari/537.36'),
           'referer': 'http://stats.nba.com/scores/',
           'connection':'keep-alive'}
r = requests.get('http://stats.nba.com/stats/commonallplayers/?',headers = HEADERS, params = {'LeagueID':'00','Season':'2015-16','IsOnlyCurrentSeason':'0'})

playerContent = r.json()

sqlite_file = "../../db.sqlite3"
#with open("players.txt", "rb") as fin:
#    content = json.load(fin)
resultSet =  playerContent["resultSets"][0]["rowSet"]
#   Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
print 'DONE with first request'
oldPlayerID = 0
for player in resultSet:
    if(player[5] == '2016'):


        playerID = int(player[0])
        playerName = player[2]
        playerName = playerName.replace(u"'",u"")
        teamID = player[10]
        #print playerID
        if((playerID != oldPlayerID)&(teamID != '')):
            r2 = requests.get('http://stats.nba.com/stats/playergamelog/?',headers = HEADERS, params = {'PlayerId':player[0],'LeagueID':'00','Season':'2015-16','SeasonType':'Regular Season'})
            playerSpecificGameData = r2.json()
            rowset2 = playerSpecificGameData["resultSets"][0]["rowSet"]
            for game in rowset2:
                gameID = game[2]
                pointsScored = game[24]

                #check if this game has already been DONE
                checkQuery = "SELECT * FROM Games WHERE id={}".format(gameID)
                c.execute(checkQuery)
                queryResult = c.fetchone()
                if(queryResult == None):
                    r3 = requests.get('http://stats.nba.com/stats/boxscoresummaryv2/?',headers = HEADERS, params = {'GameID':gameID})
                    gameSpecificData = r3.json()
                    lastMeeting = gameSpecificData["resultSets"][6]["rowSet"][0]


                    homeInfo = gameSpecificData["resultSets"][5]["rowSet"][0]
                    awayInfo = gameSpecificData["resultSets"][5]["rowSet"][1]
                    homeTeamID = homeInfo[4]
                    awayTeamID = awayInfo[4]
                    homePoints = homeInfo[22]
                    awayPoints = awayInfo[22]
                    gameSummary = gameSpecificData["resultSets"][0]["rowSet"][0]
                    date = gameSummary[0]
                    date = date.replace('T',' ')
                    winner = ""
                    if(homePoints > awayPoints):
                        winner = 'home'
                    else:
                        winner = 'away'
                    #print("{} {} {} {} {} {} {} {} {}".format(playerName,pointsScored,homeTeamID,homePoints,awayTeamID,awayPoints,date,winner, gameID))
                    gamesQuery = "INSERT INTO Games(id,date,winning_team,away_team_id_id,home_team_id_id) SELECT {4},'{0}','{1}','{2}','{3}' WHERE NOT EXISTS (SELECT * FROM Games WHERE id = {4} OR(away_team_id_id = '{2}' AND home_team_id_id = '{3}' AND date = '{0}'))".format(date,winner,awayTeamID,homeTeamID,gameID)
                    #print gamesQuery
                    c.execute(gamesQuery)

                    gameScoreQuery ="INSERT INTO GameScore(id,date,home_score,away_score,away_team_id_id,home_team_id_id) SELECT {5},'{0}',{1},{2},'{3}','{4}' WHERE NOT EXISTS (SELECT * FROM GameScore WHERE id = {5} OR (away_team_id_id = '{3}' AND home_team_id_id = '{4}' AND date = '{0}'))".format(date,homePoints,awayPoints,awayTeamID,homeTeamID,gameID)
                    c.execute(gameScoreQuery)
                else:
                    #get the date from the games that already exists
                    date = queryResult[1]
                    homeTeamID = queryResult[4]
                    awayTeamID = queryResult[3]

                playsInQuery = "INSERT INTO PlaysIn (id,date,points_scored,player_id_id,away_team_id_id,home_team_id_id) SELECT NULL, '{0}',{1},'{2}','{3}','{4}' WHERE NOT EXISTS (SELECT * FROM PlaysIn WHERE away_team_id_id = '{3}' AND home_team_id_id = '{4}' AND date = '{0}' AND player_id_id = '{2}')".format(date,pointsScored,playerID,awayTeamID,homeTeamID)
                print playsInQuery
                c.execute(playsInQuery)
                r3.close()




            r2.close()

        oldPlayerID = int(playerID)
        #print oldPlayerID
conn.commit()
conn.close()
