#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM game")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player")
    DB.commit()
    DB.close()



def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM player")
    count =  c.fetchone()
    DB.close()

    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player (name) values (%s)",(name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM standings")
    standings = c.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    player_1 = min(winner,loser)
    player_2 = max(winner, loser)
    DB = connect()
    c = DB.cursor()
    # c.execute("UPDATE game SET player_1 = %s, player_2 = %s, winner = %s WHERE player_1=",(player_1,player_2, winner))
    c.execute("INSERT into game (player_1, player_2, winner) values (%s, %s, %s)", (player_1,player_2, winner))
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM game")
    count = c.fetchone()


    if(count[0]==0):

        c = DB.cursor()
        c.execute("SELECT * FROM player")
        players = c.fetchall()
        standings = players
    else:
        standings = playerStandings()

    DB.close()

    pairings = []



    for i in  xrange(0,len(standings),2):
        pairings.append((standings[i][0],standings[i][1], standings[i+1][0],standings[i+1][1]))

    return pairings



