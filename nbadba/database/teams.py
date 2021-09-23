import requests
import json

import sqlite3
HEADERS = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/57.0.2987.133 Safari/537.36'),
           'referer': 'http://stats.nba.com/scores/',
           'connection':'keep-alive'}
r = requests.get('http://stats.nba.com/stats/commonTeamYears/?',headers = HEADERS, params = {'LeagueID':'00'})

teamContent = r.json()#all the teams and their ids
sqlite_file = "database.sqlite"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
resultSet = teamContent['resultSets'][0]['rowSet']
for team in resultSet:
    if(team[3] == '2016'):
        #TeamID, TeamName, City, rankNum, Conference, numWins, numLosses
        teamID = team[4]
        r2 = requests.get('http://stats.nba.com/stats/teaminfocommon/?',headers = HEADERS, params = {'Season':'2015-16','TeamID':team[1],'LeagueID':'00','SeasonType':'Regular Season'})

        #detailed info about this team
        fullContent = r2.json()
        resultSet = fullContent['resultSets'][0]['rowSet'][0]
        teamName = resultSet[3]
        city = resultSet[2]
        rank = resultSet[11]
        conference = resultSet[5]
        numWins = resultSet[8]
        numLosses = resultSet[9]

        query = "INSERT INTO Teams VALUES ('{}','{}','{}',{},'{}',{},{})".format(teamID, teamName, city, rank, conference, numWins, numLosses)
        print query
        c.execute(query)
        r2.close()
conn.commit()
conn.close()
