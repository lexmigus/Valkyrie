"""
This module provides a graphical user interface for managing a user database.
It allows users to insert, remove, update, and retrieve user information

Functions:
- create_table(): Create the users table in the database.
- update_pb(user_id, option, pb): Update the PB of a user for a specific workout.
- execute_sql(sql, params=None): Connect to the database and execute an SQL command.
"""

from os import listdir, remove
from sqlite3 import connect, Error
import PySimpleGUI as sg


def create_table():
    """Create the users table in the database."""
    con = connect("data/user_database.db")
    marker = con.cursor()
    marker.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            lightweight BOOLEAN,
            novice BOOLEAN
            One_Minute TEXT,
            One_KM TEXT,
            Two_KM TEXT,
            Six_KM TEXT,
            Hour TEXT,
            Fourx1K TEXT,
            Threex6k TEXT,
            Threex12Min TEXT,
            Threex30Min TEXT,
            Peak_Power INTEGER
        )
    """
    )
    con.commit()
    con.close()


def update_pb(uid, workout, pr):
    """Update the PB of a user for a specific workout"""
    con = connect("data/user_database.db")
    marker = con.cursor()
    marker.execute(f"UPDATE users SET {workout} = ? WHERE user_id = ?", (pr, uid))
    con.commit()
    con.close()


# Create the users table
create_table()
# Define the layout of the window
layout = [
    [sg.Text("User Database", font=("Arial", 20))],
    [
        sg.Text("User ID:"),
        sg.Input(key="-ID-"),
        sg.Button("Insert", key="-INSERT-"),
        sg.Button("Remove", key="-REMOVE-"),
    ],
    [sg.Text("Name:  "), sg.Input(key="-NAME-")],
    [sg.Checkbox("Lightweight", default=False, key="-LIGHTWEIGHT-")],
    [sg.Checkbox("Novice", default=False, key="-NOVICE-")],
    [
        sg.Combo(
            [
                "Peak_Power",
                "One_Minute",
                "One_KM",
                "Two_KM",
                "Six_KM",
                "Hour",
                "Fourx1K",
                "Threex6k",
                "Threex12Min",
                "Threex30Min",
            ],
            key="-OPTION-",
            enable_events=True,
        ),
        sg.Input(key="-PB-"),
        sg.Button("Update PB", key="-Update-PB-"),
    ],
    [
        sg.Button("Get List of Users", key="-GET-LIST-"),
        sg.Button("Get List of PBs", key="-GET-PB-"),
    ],
    [sg.Output(size=(60, 10), key="-OUTPUT-")],
    [sg.Button("Exit")],
]


# Create the window object
window = sg.Window("User Database", layout, icon="resources/VarsityV.ico")


# Create a function to connect to the database and execute SQL commands
def execute_sql(sql, params=None):
    """Connect to the database and execute an SQL command."""
    # Connect to the database
    con = connect("data/user_database.db")
    # Create a cursor object to execute SQL commands
    marker = con.cursor()
    # Execute the SQL command with or without parameters
    if params:
        marker.execute(sql, params)
    else:
        marker.execute(sql)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Create a loop to read the events and values from the window
while True:
    event, values = window.read()
    # If the user closes the window, break the loop
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    # If the user clicks the Insert button, insert the user ID and name to the database
    elif event == "-INSERT-":
        user_id = values["-ID-"]
        name = values["-NAME-"]
        lightweight = values["-LIGHTWEIGHT-"]
        novice = values["-NOVICE-"]
        if user_id and name:
            try:
                execute_sql(
                    "INSERT INTO users (user_id, name, lightweight, novice) VALUES (?, ?, ?, ?)",
                    (user_id, name, lightweight, novice),
                )
                print(
                    f"User ID {user_id}, name {name}, lightweight {lightweight}, and novice {novice} inserted successfully."
                )
                window["-ID-"].update("")
                window["-NAME-"].update("")
                window["-LIGHTWEIGHT-"].update(False)
                window["-NOVICE-"].update(False)

            except Error as e:
                print(f"Error: {e}")
        else:
            print("Please enter a user ID and a name.")

    # If the user clicks the Remove button, remove the user ID from the database
    elif event == "-REMOVE-":
        user_id = values["-ID-"]
        if user_id:
            try:
                execute_sql("DELETE FROM users WHERE user_id = ?", (user_id,))
                print(f"User ID {user_id} removed successfully.")
                window["-ID-"].update("")
                window["-NAME-"].update("")
                window["-LIGHTWEIGHT-"].update(False)
                window["-NOVICE-"].update(False)
                if f"{user_id}.json" in listdir("data"):
                    remove(f"data/{user_id}.json")
            except Error as e:
                print(f"Error: {e}")
        else:
            print("Please enter a user ID.")

    elif event == "-Update-PB-":
        user_id = values["-ID-"]
        option = values["-OPTION-"]
        pb = values["-PB-"]
        try:
            update_pb(user_id, option, pb)
            print(f"User ID {user_id} updated successfully.")
            window["-OPTION-"].update("")
            window["-PB-"].update("")
        except Error as e:
            print(f"Error: {e}")
        else:
            print("Please enter a user ID, a PB option, and a PB.")

    elif event == "-GET-LIST-":
        try:
            # Connect to the database
            conn = connect("data/user_database.db")
            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()
            # Get all data from the users table
            cursor.execute("SELECT * FROM users")
            # Fetch the results
            users = cursor.fetchall()
            # Close the connection
            conn.close()
            # Print the user data
            print("The user data is:")
            for user in users:
                data = f"{user[0]}: {user[1]}"
                if user[2]:
                    data += ", Lightweight"
                if user[3]:
                    data += ", Novice"
                print(data)
        except Error as e:
            print(f"Error: {e}")

    elif event == "-GET-PB-":
        try:
            conn = connect("data/user_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            conn.close()
            print("The Vikes' PB's Are:")
            for user in users:
                print(
                    f"{user[1]}: 1min: {user[4]}, 1km: {user[5]}, 2km: {user[6]}, 6km: {user[7]}, 60min: {user[8]}m, 4x1km: {user[9]}, 3x6km: {user[10]}, 3x12min: {user[11]}m, 3x30min: {user[12]}, Peak Power: {user[13]}watts\n"
                )
        except Error as e:
            print(f"Error: {e}")

# Close the window
window.close()
