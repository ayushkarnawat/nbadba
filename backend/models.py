# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# CREATE TABLE Teams (
#       TeamID varchar(3), 
#       TeamName varchar(20), 
#       HomeCity varchar(20), 
#       Rank INT, 
#       Conference ENUM(‘EASTERN’,’WESTERN’), 
#       numWins INT, 
#       numLosses INT, 
#       PRIMARY KEY (TeamID)
# );
class Team(models.Model):
    team_id = models.CharField(max_length=3, primary_key=True)
    team_name = models.CharField(max_length=20)
    home_city = models.CharField(max_length=20)
    rank = models.IntegerField()
    CONFERENCE_CHOICES = (
        ('EAST', 'EASTERN'),
        ('WEST', 'WESTERN')
    )
    conference = models.CharField(max_length=4, choices=CONFERENCE_CHOICES, default=None)
    num_wins = models.IntegerField();
    num_losses = models.IntegerField();

    def __str__(self):
        return self.team_id + ": " + self.home_city + " " + self.team_name

    def __unicode__(self):
        return self.team_id + ": " + self.home_city + " " + self.team_name

    class Meta:
        db_table = 'Teams'

# CREATE TABLE Players (
#       PlayerID char(5), 
#       PlayerName varchar(30), 
#       age int, 
#       TeamID varchar(3), 
#       Role varchar(20)), 
#       PRIMARY KEY(PlayerID), 
#       FOREIGN KEY(TeamID) REFERENCES Teams (TeamID)
# );
class Player(models.Model):
    player_id = models.CharField(max_length=10, primary_key=True)
    player_name = models.CharField(max_length=30)
    height = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.player_id

    def __unicode__(self):
        return self.player_id

    class Meta:
        db_table = 'Players'

# CREATE TABLE GameScore (
#       Date date, 
#       HomeTeamID varchar(3), 
#       AwayTeamID varchar(3), 
#       homeScore INT, 
#       awayScore INT, 
#       PRIMARY KEY (Date, HomeTeamID, AwayTeamID), 
#       FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), 
#       FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID)
# );
class GameScore(models.Model):
    date = models.DateField(blank=True, null=True)  # Field name made lowercase.
    home_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='home_team')  # Field name made lowercase.
    away_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='away_team')  # Field name made lowercase.
    home_score = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    away_score = models.IntegerField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.date) + ": "+ self.home_team_id.team_name + " vs. " + self.away_team_id.team_name

    def __unicode__(self):
        return str(self.date) + ": "+ self.home_team_id.team_name + " vs. " + self.away_team_id.team_name

    class Meta:
        db_table = 'GameScore'
        unique_together = (('date', 'home_team_id', 'away_team_id'),)
    

# CREATE TABLE Games (
#       Date date, 
#       HomeTeamID varchar(3), 
#       AwayTeamID varchar(3), 
#       winningTeam ENUM(‘HOME’,’AWAY’), 
#       PRIMARY KEY (Date, HomeTeamID, AwayTeamID), 
#       FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID)
#       FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID)
# );
class Game(models.Model):
    date = models.DateField(blank=True, null=True)  # Field name made lowercase.
    home_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='home_team_game')
    away_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='away_team_game')
    WINNING_TEAM_CHOICES = (
        ('HOME', 'Home Team'),
        ('AWAY', 'Away Team')
    )
    winning_team = models.CharField(max_length=20, choices=WINNING_TEAM_CHOICES, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.date) + ": "+ self.home_team_id.team_name + " vs. " + self.away_team_id.team_name

    def __unicode__(self):
        return str(self.date) + ": "+ self.home_team_id.team_name + " vs. " + self.away_team_id.team_name

    class Meta:
        db_table = 'Games'
        unique_together = (('date', 'home_team_id', 'away_team_id'),)

# CREATE TABLE Coach (
#       coachID varchar(5), 
#       CoachName varchar(30), 
#       age int, 
#       TeamID varchar(3), 
#       PRIMARY KEY (coachID), 
#       FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
# );
class Coach(models.Model):
    coach_id = models.CharField(max_length=5, primary_key=True)  # Field name made lowercase.
    coach_name = models.CharField(max_length=30, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.coach_id + ": " + self.coach_name

    def __unicode__(self):
        return self.coach_id + ": " + self.coach_name

    class Meta:
        db_table = 'Coaches'

# CREATE TABLE Owner (
#       ownerID varchar(5), 
#       OwnerName varchar(30), 
#       age int, 
#       netWorth int, 
#       TeamID varchar(3), 
#       PRIMARY KEY (ownerID), 
#       FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
# );
class Owner(models.Model):
    owner_id = models.CharField(max_length=5, primary_key=True)  # Field name made lowercase.
    owner_name = models.CharField(max_length=30, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(blank=True, null=True)
    networth = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.owner_id + ": " + self.owner_name

    def __unicode__(self):
        return self.owner_id + ": " + self.owner_name

    class Meta:
        db_table = 'Owners'

# CREATE TABLE PlaysIn (
#       PlayerID varchar(5), 
#       Date date, 
#       HomeTeamID varchar(3), 
#       AwayTeamID varchar(3), 
#       PointsScored int, 
#       PRIMARY KEY (PlayerID, Date, HomeTeamID, AwayTeamID), 
#       FOREIGN KEY (PlayerID) REFERENCES Players (PlayerID), 
#       FOREIGN KEY (HomeTeamID) REFERENCES Teams (TeamID), 
#       FOREIGN KEY (AwayTeamID) REFERENCES Teams (TeamID), 
#       FOREIGN KEY (Date, HomeTeamID, AwayTeamID) REFERENCES Games (Date, HomeTeamID, AwayTeamID)
# );
class PlaysIn(models.Model):
    player_id = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)  # Field name made lowercase.
    home_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='home_team_playsin')  # Field name made lowercase.
    away_team_id = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, related_name='away_team_playsin')  # Field name made lowercase.
    points_scored = models.IntegerField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.player_id.player_name + " Plays In: " + self.date + ", Home Team ID: " + self.home_team + ", Away Team ID: " + self.away_team

    class Meta:
        db_table = 'PlaysIn'
        unique_together = (('player_id', 'date', 'home_team_id', 'away_team_id'),)