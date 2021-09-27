import sqlite3

from nbadba.settings import DATABASES

# import requests
# HEADERS = {
#     "user-agent": (
#         "Mozilla/5.0 (Windows NT 10.0; WOW64)"
#         "AppleWebKit/537.36 (KHTML, like Gecko)"
#         "Chrome/57.0.2987.133 Safari/537.36"
#     ),
#     "referer": "https://github.com",
#     "connection": "keep-alive",
# }
# res = requests.get(
#     "http://stats.nba.com/stats/commonallplayers/?",
#     headers=HEADERS,
#     params={
#         "LeagueID": "00",
#         "Season": "2015-16",
#         "IsOnlyCurrentSeason": "0",
#     }
# )

sqlite_file = "../db.sqlite3"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
query = "SELECT * FROM Games WHERE id='21501160'"
c.execute(query)
print(c.fetchone())
conn.commit()
conn.close()
