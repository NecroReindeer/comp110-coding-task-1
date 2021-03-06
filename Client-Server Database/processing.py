"""Store functions for processing data.

This module contains functions for processing data and
accessing the database.
"""

import cgi

import pymysql


def get_player_name(form):
    """Return the player name from the form to be used in the database.

    This function retrieves the player name from the form and formats it
    so that it is consistent with the database entries. It then returns
    the player name as a string.
    """

    if "player" not in form:
        return None
    else:
        player_name = str(form.getvalue("player")).upper()
        player_name = chop_name(player_name, 3)
        return player_name


def get_level_number(form):
    """Return the level number from the form.

    This function retrieves the level number from the form
    and returns it as a string.
    """

    if "level" not in form:
        return None
    else:
        level_number = form.getvalue("level")
        return level_number


def get_score(form):
    """Return the score from the form.

    This function retrieves the score from the form
    and returns it as a string.
    """

    if "score" not in form:
        return None
    else:
        score = form.getvalue("score")
        return score


def get_new_name(form):
    """Return the player name from the form to be used in the database.

    This function retrieves the player name from the form and formats it
    so that it is consistent with the database entries. It then returns
    the player name as a string.
    """

    if "new" not in form:
        return None
    else:
        new_name = str(form.getvalue("new")).upper()
        new_name = chop_name(new_name, 3)
        return new_name


def chop_name(name, characters):
    """Return a name stripped down to the given number of characters."""

    chopped_name = name[:characters]
    return chopped_name


def get_player_id(player_name):
    """Return the player id corresponding to the given name.

    This function retrieves the player id corresponding to the
    given name from the database, and returns it as a string.
    """

    # Connect to the database
    connection, cursor = connect_to_database()

    cursor.execute("SELECT player_id FROM players "
                   "WHERE player_name=%s", (player_name,))
    player_id = [row[0] for row in cursor.fetchall()]

    if len(player_id) != 0:
        # Convert to string for consistency
        return str(player_id[0])
    else:
        return None


def username_is_unique(username):
    """Check if a username does not already exist.

    This function checks if a username does not already
    exist in the players table. If the user doesn't
    already exist, it returns True. Otherwise, it returns False.
    """

    connection, cursor = connect_to_database()
    # Get list of all existing users
    cursor.execute("SELECT player_name FROM players")
    existing_users = [(row[0]) for row in cursor.fetchall()]

    # Only one of each name will be allowed
    if username not in existing_users:
        return True
    else:
        return False


def add_level(level_number):
    """Add a level of a given number to the database.

    This function adds a level of the given number to the database.
    The level number will be used as the primary key, and the level
    name will correspond to the level number.
    """

    connection, cursor = connect_to_database()
    level_name = "Level " + level_number
    cursor.execute("INSERT INTO levels VALUES(%s, %s)", (level_number, level_name))
    connection.commit()


def connect_to_database():
    """Connect to the database.

    This function connects to the highscores database and
    returns the cursor and connection.
    """

    connection = pymysql.connect(
            db='highscores',
            user='root',
            passwd='falser110',
            host='localhost')
    cursor = connection.cursor()
    return connection, cursor

