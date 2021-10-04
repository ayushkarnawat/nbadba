import os

import coaches
import games
import players
import teams


def make_sqlite(filepath: str, warn: bool = True) -> None:
    """Make (barebones) SQLite3 database for the 2015-16 season."""
    # Does the filename have a canonical sqlite-compatible extension?
    filepath = os.path.abspath(filepath)
    filename, ext = os.path.splitext(filepath)
    recommended_exts = [".db", ".sdb", ".sqlite", ".db3", ".s3db", ".sqlite3",
                        ".sl3", ".db2", ".s2db", ".sqlite2", ".sl2"]
    if ext not in recommended_exts and warn:
        raise ValueError(
            f"The database file '{filepath}' should end in a compatible " +
            f"extension. Please use one of the following formats: " +
            f"{recommended_exts}. If you wish to use a non-standard file " +
            f"format, set warn=False."
        )

    if os.path.exists(filepath):
        print(f"File '{filepath}' already exists, exiting...")
        return
    else:
        import sqlite3
        conn = sqlite3.connect(filepath)
        c = conn.cursor()

        # Create all tables
        c.execute(
            """
            CREATE TABLE Teams ( \
                TeamID varchar(3), \
                TeamName varchar(20), \
                HomeCity varchar(20), \
                rankNum INT, \
                Conference varchar(20), \
                numWins INT, \
                numLosses INT, \
                PRIMARY KEY (TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE Players ( \
                PlayerID varchar(10), \
                PlayerName varchar(30), \
                height varchar(10), \
                TeamID varchar(3), \
                Role varchar(20), \
                PRIMARY KEY(PlayerID), \
                FOREIGN KEY(TeamID) REFERENCES Teams(TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE Coach ( \
                coachID varchar(10), \
                CoachName varchar(30), \
                age int, \
                TeamID varchar(3), \
                PRIMARY KEY (coachID), \
                FOREIGN KEY (TeamID) REFERENCES Teams (TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE Owner ( \
                ownerID varchar(10), \
                OwnerName varchar(30), \
                age int, \
                netWorth int, \
                TeamID varchar(3), \
                PRIMARY KEY (ownerID), \
                FOREIGN KEY (TeamID) REFERENCES Teams (TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE Games ( \
                Date date, \
                HomeTeamID varchar(3), \
                AwayTeamID varchar(3), \
                winningTeam varchar(20), \
                PRIMARY KEY (Date, HomeTeamID, AwayTeamID), \
                FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), \
                FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE GameScore ( \
                Date date, \
                HomeTeamID varchar(3), \
                AwayTeamID varchar(3), \
                homeScore INT, \
                awayScore INT, \
                PRIMARY KEY (Date, HomeTeamID, AwayTeamID), \
                FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), \
                FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID) \
            )
            """
        )

        c.execute(
            """
            CREATE TABLE PlaysIn ( \
                PlayerID varchar(10), \
                Date date, \
                HomeTeamID varchar(3), \
                AwayTeamID varchar(3), \
                PointsScored int, \
                PRIMARY KEY (PlayerID, Date, HomeTeamID, AwayTeamID), \
                FOREIGN KEY (PlayerID) REFERENCES Players (PlayerID), \
                FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), \
                FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID), \
                FOREIGN KEY (Date, HomeTeamID, AwayTeamID) \
                    REFERENCES Games (Date, HomeTeamID, AwayTeamID) \
            )
            """
        )

        # Retrieve all information of interest (using API) and insert into db
        team_data = teams.get_team_info(
            season="2015-16", season_type="Regular Season", leauge_id="00",
        )
        for (team_id, city, team_name, conference, num_wins, num_losses, rank) \
                in team_data:
            query = f"""
            INSERT INTO Teams VALUES ('{team_id}', '{team_name}', '{city}',
                {rank}, '{conference}', {num_wins},{ num_losses})
            """
            c.execute(query)

        player_data = players.get_player_info(season="2015-16", leauge_id="00",)
        for (player_id, player_name, height, team_id, position) in player_data:
            query = f"""
            INSERT INTO Players VALUES ('{player_id}', '{player_name}', \
                '{height}', '{team_id}', '{position}')
            """
            c.execute(query)

        coach_data = coaches.get_coach_info(
            season="2015-16", season_type="Regular Season", leauge_id="00",
        )
        for (coach_id, coach_name, coach_type, team_id) in coach_data:
            query = """
            INSERT INTO Coaches
            SELECT '{1}','{3}','{2}','{0}'
            WHERE NOT EXISTS (
                SELECT *
                FROM Coaches
                WHERE coach_id = '{0}'
            )
            """.format(coach_id, coach_name, coach_type, team_id)
            c.execute(query)

        # TODO: Insert owner info
        # Unfortunately, stats.nba.com does not have an endpoint for retriving
        # owner info, so the process must be done manually by checking wiki.

        games_data = games.get_game_info(
            season="2015-16", season_type="Regular Season", leauge_id="00",
        )
        for (game_id, date, away_team_id, home_team_id, away_points,
                home_points, winner, _) in games_data:
            games_query = """
            INSERT INTO Games(id, date, winning_team,
                            away_team_id_id, home_team_id_id) \
            SELECT {4},'{0}','{1}','{2}','{3}'
            WHERE NOT EXISTS (
                SELECT *
                FROM Games
                WHERE id = {4}
                    OR (away_team_id_id = '{2}'
                    AND home_team_id_id = '{3}'
                    AND date = '{0}'
                )
            )
            """.format(date, winner, away_team_id, home_team_id, game_id)
            c.execute(games_query)

            game_score_query = """
            INSERT INTO GameScore(id, date, home_score, away_score,
                                away_team_id_id, home_team_id_id)
            SELECT {5},'{0}',{1},{2},'{3}','{4}'
            WHERE NOT EXISTS (
                SELECT *
                FROM GameScore
                WHERE id = {5}
                    OR (away_team_id_id = '{3}'
                    AND home_team_id_id = '{4}'
                    AND date = '{0}')
            )
            """.format(
                date,
                home_points,
                away_points,
                away_team_id,
                home_team_id,
                game_id,
            )
            c.execute(game_score_query)

        player_game_data = games.get_player_specific_game_info(
            season="2015-16", season_type="Regular Season", leauge_id="00",
        )
        for (player_id, date, away_team_id, home_team_id, points_scored) \
                in player_game_data:
            plays_in_query = """
            INSERT INTO PlaysIn(id, date, points_scored, player_id_id,
                                away_team_id_id, home_team_id_id)
            SELECT NULL, '{0}',{1},'{2}','{3}','{4}'
            WHERE NOT EXISTS (
                SELECT *
                FROM PlaysIn
                WHERE away_team_id_id = '{3}'
                    AND home_team_id_id = '{4}'
                    AND date = '{0}'
                    AND player_id_id = '{2}'
            )
            """.format(date, points_scored, player_id, away_team_id, home_team_id)
            c.execute(plays_in_query)

        # Save and close file
        conn.commit()
        conn.close()

if __name__ == "__main__":
    make_sqlite("nba_small.db", warn=True)
