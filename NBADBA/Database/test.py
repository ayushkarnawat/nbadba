import requests
import sqlite3
HEADERS = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/57.0.2987.133 Safari/537.36'),
           'referer': 'http://stats.nba.com/scores/',
           'connection':'keep-alive'}
#r = requests.get('http://stats.nba.com/stats/commonallplayers/?LeagueID=00&Season=2015-16&IsOnlyCurrentSeason=0',headers = HEADERS)


sqlite_file = "../../db.sqlite3"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
query = "SELECT * FROM Games WHERE id='77';"
c.execute(query)
query = "SELECT * FROM Games WHERE id='77';"
c.execute(query)
print c.fetchone()[1];
conn.commit()
conn.close()
