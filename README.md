## Basketball Statistics Dashboard
Display and aggregate information about games, teams, players,
coaches, and owners from the National Basketball Association (NBA).

Although one can view recent statistics on [NBA's
website](https://stats.nba.com), there are use cases (for both developers and
end users) where this project might be useful. In particular, having an
queryable API and a (basic) database design gives developers a starting point to
develop more visualizations with greater flexibility, write complex SQL commands
to aggregate information in interesting ways, etc. End users could then use this
new information to gain more insight into the data.


## Build
  1. Clone or download the project
  2. Install all required packages using `requirements.txt` (ideally within a
     virtual environment)
  3. Run `python manage.py runserver` to activate the server from a shell
  4. View application on port 8000: `http://localhost:8000`

Despite the fact that datasets can becomes quite large (upto ~100MB per season
depending on the data we are interested in logging), we provide a small
populated (SQLite) datatbase for the 2015-16 NBA season, only to be used locally
for developmental purposes.

It is recommended, however, to use the scripts provided to automatically
populate a client-server database (e.g. PostgresSQL, MySQL) in a cloud-based
environment (e.g. Amazon RDS). See `database/` folder for more details.


## Overview

To populate a barebones version of the database (see design below), we
programatically query endpoints provided by the NBA (e.g. for
[teams](https://stats.nba.com/stats/commonteamroster?LeagueID=&Season=2019-20&TeamID=1610612739)
and
[players](https://stats.nba.com/stats/commonplayerinfo?LeagueID=&PlayerID=2544)).

![Database ontology](assets/entity_relationship_diagram.pdf)

### Teams

The `Teams` table records information about teams. In particular, we log the
team id (primary key), home city, team name, which conference they play in,
their current rank with respect to the other teams in that conference, and
number of wins and losses (up to this point in the season).

Each team consists of players, coaches, owners, each of which are referenced via
foreign keys in their respective table. In addition, every season, each team
plays in a certain predefined amount of regular season games.

### Players

The `Players` table records basic information about each player (active or
inactive). We save the player id (primary key), their name, their age, which
team they play on (by team id), and their specific role within that team.

It is important to note that not every player plays in every game for the team
(e.g. players can be injured, not get put into the game by the coach). As such,
we have a seperate DB table (aptly named `PlaysIn`) which handles which player
played in what game.

### Coaches

The `Coaches` table records all the (head, assistant, developmental) coaches. For
each coach, we have a unique id (primary key), their name, their age, and the
team they are associated with (referenced by the team id foreign key).

### Owners

The `Owners` table records the majority and minority stakeholders who
collectively own a team. Each owner has their own unique id (primary key), their
name, their age, their networth, and which team they have a stake in (referenced
by the team id foreign key).

Note that there can be multiple owners for a single team, and that (legally)
a person can only have a stake in one team at a time.

### Game

The `Games` table records all the stats from each regular/post season game in
the specified season. Here we record the date the game occurred, the teams
playing in that game, and the winning team (either home or away). Since each
team can play multiple times within a season, the primary key is the combination
of both team ids and the date when they played.

Other information about the game (e.g. total points, assists, rebounds, etc.)
logged by each team is stored in a seperate DB table (GameScore).


## TODO
- [ ] Main page
  - [ ] Display info about games from latest date (or last day of the season).
  - [ ] Include score, team names, team logo, venue, etc.
  - [ ] Panel for daily leaders, e.g. pts, assists, rebounds, etc.
- [ ] Teams overview
  - [ ] Two column (Eastern and Western conference)
  - [ ] Teams ordered by rank, wins/loss record, last 10
- [ ] Player overview
  - [ ] List players by alphabetical order (grouping by A-Z)
- [ ] Games overview
  - [ ] Toggle for calendar views (day, week, month, year)
  - [ ] Display less/more information about games depending on which is chosen


## Acknowledgements
The dashboard was developed by Rahul Pokharna, Sibi Sengottuvel, and Ayush
Karnawat.
