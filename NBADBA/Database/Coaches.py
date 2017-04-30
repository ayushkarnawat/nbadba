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
sqlite_file = "db.sqlite3"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
resultSet = teamContent['resultSets'][0]['rowSet']
for team in resultSet:
    if(team[3] == '2016'):
        #coach_id,coach_name,type,team_id
        teamID = team[4]
        r2 = requests.get('http://stats.nba.com/stats/commonteamroster/?',headers = HEADERS, params = {'Season':'2015-16','TeamID':team[1],'LeagueID':'00','SeasonType':'Regular Season'})

        #detailed info about this team
        fullContent = r2.json()
        resultSet2 = fullContent['resultSets'][1]['rowSet']
        print resultSet2
        for coach in resultSet2:
        
            coachID = coach[2]
            coachName = coach[5]
            coachName = coachName.replace(u"'",u"")
            coachType = coach[8]
            query = "INSERT INTO Coaches SELECT '{0}','{1}','{2}','{3}' WHERE NOT EXISTS (SELECT * FROM Coaches WHERE coach_id = '{0}')".format(coachID, coachName, coachType, teamID)
            print query
            c.execute(query)

        

        
        r2.close()
conn.commit()
conn.close()
