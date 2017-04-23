
import sqlite3

sqlite_file = 'database.sqlite'    # name of the sqlite database file


#   Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("CREATE TABLE Teams (TeamID varchar(3), TeamName varchar(20), HomeCity varchar(20), rankNum INT, Conference varchar(20), numWins INT, numLosses INT, PRIMARY KEY (TeamID))")


c.execute("CREATE TABLE Players (PlayerID varchar(10), PlayerName varchar(30), firstYear int, TeamID varchar(3), Role varchar(20), PRIMARY KEY(PlayerID) FOREIGN KEY(TeamID) REFERENCES Teams(TeamID))")


c.execute("CREATE TABLE GameScore (Date date, HomeTeamID varchar(3), AwayTeamID varchar(3), homeScore INT, awayScore INT, PRIMARY KEY (Date, HomeTeamID, AwayTeamID), FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID))")

c.execute("CREATE TABLE Games (Date date, HomeTeamID varchar(3), AwayTeamID varchar(3), winningTeam varchar(20), PRIMARY KEY (Date, HomeTeamID, AwayTeamID) FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID),  FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID))")

c.execute("CREATE TABLE Coach (coachID varchar(10), CoachName varchar(30), age int, TeamID varchar(3), PRIMARY KEY (coachID), FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))")

c.execute("CREATE TABLE Owner (ownerID varchar(10), OwnerName varchar(30), age int, netWorth int, TeamID varchar(3), PRIMARY KEY (ownerID), FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))")

c.execute("CREATE TABLE PlaysIn (PlayerID varchar(10), Date date, HomeTeamID varchar(3), AwayTeamID varchar(3), PointsScored int, PRIMARY KEY (PlayerID, Date, HomeTeamID, AwayTeamID) FOREIGN KEY (PlayerID) REFERENCES Players (PlayerID), FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID), FOREIGN KEY (Date, HomeTeamID, AwayTeamID) REFERENCES Games (Date, HomeTeamID, AwayTeamID))")

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
