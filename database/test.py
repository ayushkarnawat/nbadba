import sqlite3

sqlite_file = "nba_small.db"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

query = "SELECT * FROM PlaysIn"
c.execute(query)
print(c.fetchone())
c.close()
conn.commit()
conn.close()
