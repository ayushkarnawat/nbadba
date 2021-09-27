import sqlite3

sqlite_file = "db.sqlite3"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

query = "SELECT * FROM PlaysIn"
c.execute(query)
for result in c.fetchall():
    update = "UPDATE PlaysIn set date = '{}' WHERE id = {}".format(
        result[1].split(" ")[0], # date
        result[0], # game_id
    )
    c.execute(update)
c.close()
conn.commit()
conn.close()
