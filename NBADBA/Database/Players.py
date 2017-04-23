import urllib2
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

sqlite_file = "database.sqlite"
#with open("players.txt", "rb") as fin:
#    content = json.load(fin)
resultSet =  playerContent["resultSets"][0]["rowSet"]
#   Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
print 'DONE with first request'
for player in resultSet:
    oldPlayerName = ' '
    if(player[5] == '2016'):
        #playerID, playerName, height, TeamID, Role
        #get the team roster for this Team

        playerID = player[0]
        playerName = player[2]
        playerName = playerName.replace(u"'",u"")
        if(playerName != oldPlayerName):
            r2 = requests.get('http://stats.nba.com/stats/commonplayerinfo/?',headers = HEADERS, params = {'PlayerId':player[0]})
            playerSpecific = r2.json()
            resultSet2 = playerSpecific["resultSets"][0]["rowSet"]
            height = resultSet2[0][10]
            position = resultSet2[0][14]
            teamID = player[10]
            query = "INSERT INTO Players VALUES ('{}','{}','{}','{}','{}')".format(playerID, playerName, height, teamID, position)
            print query
            c.execute(query)
        oldPlayerName = playerName
