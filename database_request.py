"""
This module provides functions for interacting with the user database.
The database contains information about users, including their IDs and names.

Functions:
    - get_list_user_ids() -> list[int]: Get a list of all user IDs.
    - get_name(user_id) -> str: Get the name of a user given their user ID.
    - get_number_users() -> int: Get the number of users in the database.
    - get_pb(user_id, option) -> int: Get the PB of a user given a user ID and option.
"""
from sqlite3 import connect


def get_list_user_ids()->list[int]:
    """Get a list of all user IDs.

    Returns:
        list: A list of all user IDs.
    """
    conn = connect("data/user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()

    formatted_user_ids = [int(item[0]) for item in user_ids]
    conn.close()
    return formatted_user_ids


def get_name(user_id: int) -> str:
    """Get the name of a user given their user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The name of the user with the given ID, or a message if no user is found.
    """
    conn = connect("data/user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return f"No user found with ID {user_id}"


def get_number_users() -> int:
    """Get the number of users in the database.

    Returns:
        int: The number of users in the database.
    """
    return len(get_list_user_ids())

def get_pb(user_id: int, option: str) -> int:
    """Get the personal best of a user given their user ID and the option.

    Args:
        user_id (int): The ID of the user.
        option (str): The option of the personal best.

    Returns:
        int: PB of the user with the given ID and option, or a message if no user is found.
    """
    conn = connect("data/user_database.db")
    cursor = conn.cursor()
    query = f"SELECT {option} FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return f"No user found with ID {user_id}"
if __name__ == "__main__":
    print(get_list_user_ids())
    print(get_name(1524007))
    print(get_number_users())
    print(get_pb(1524007, 'Peak_Power'))
    print(get_pb(1524007, 'One_Minute'))
    print(get_pb(1524007, 'One_Km'))
    print(get_pb(1524007, 'Two_Km'))
    print(get_pb(1524007, 'Six_Km'))
    print(get_pb(1524007, 'Hour'))
    print(get_pb(1524007, 'Fourx1K'))
    print(get_pb(1524007, 'Threex6k'))
    print(get_pb(1524007, 'Threex12Min'))
    print(get_pb(1524007, 'Threex30Min'))
