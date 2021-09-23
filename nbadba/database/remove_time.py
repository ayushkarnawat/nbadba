import sqlite3

sqlite_file = "db.sqlite3"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

query = "SELECT * FROM PlaysIn"
c.execute(query)
results = c.fetchall()
#print results
for result in results:
    gameID = result[0]
    date = result[1].split(' ')[0]
    print result
    update = "UPDATE PlaysIn set date = '{}' WHERE id = {}".format(date,gameID)
    c.execute(update)
c.close()
conn.commit()
conn.close()