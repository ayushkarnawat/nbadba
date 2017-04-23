from bs4 import BeautifulSoup
import json

import sqlite3
requests.get('http://stats.nba.com/stats/commonteamroster/', data={'Season':'2015-16','TeamID':'1610612739'})
sqlite_file = "database.sqlite"
with open("players.txt", "rb") as fin:
    content = json.load(fin)
resultSet =  content["resultSets"][0]["rowSet"]
#   Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

for player in resultSet:
    if(player[5] == '2016'):
        #playerID, playerName, firstYear, TeamID, Role
        #c.execute("INSERT INTO Players VALUES (player[0],'BUY','RHAT',100,35.14)")
        print player[0]
