
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db_conn = connect()
    db_cursor = db_conn.cursor()
    db_cursor.execute("delete from matches;")
    db_conn.commit() 
    db_conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db_conn = connect()
    db_cursor = db_conn.cursor()
    db_cursor.execute("delete from players;")
    db_conn.commit()
    db_conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db_conn = connect()
    db_cursor = db_conn.cursor()
    db_cursor.execute("select count(*) from players;")
    rows = db_cursor.fetchall()
    db_conn.close()
    return int(rows[0][0])   
 
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db_conn = connect()
    db_cursor = db_conn.cursor()
    name = bleach.clean(name, strip=True)
    db_cursor.execute("INSERT INTO players VALUES (DEFAULT, %s);", (name, ))
    db_conn.commit()
    db_conn.close()


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
    db_con = connect()
    db_cursor = db_con.cursor()
    db_cursor.execute("SELECT * FROM standings;")
    results = db_cursor.fetchall()
    db_con.close()

    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db_conn = connect()
    db_cursor = db_conn.cursor()
    db_cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    db_conn.commit()
    db_conn.close()
 
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
    db_con = connect()
    db_cursor = db_con.cursor()
    query = "SELECT * FROM standings;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    new_pairs = []
    stop = len(results) - 1

    for index in range(0, stop, 2):
        new_pair = (results[index][0], results[index][1], results[index + 1][0], results[index + 1][1])
        new_pairs.append(new_pair)

    db_con.close()
    return new_pairs

