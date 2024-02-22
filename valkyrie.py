"""
This module contains the main script for the Valkyrie application.
Valkyrie is a workout ranking and management tool for Concept2 rowing machines.

Functions:
- open_settings(): Open the settings window and read the values of the settings.
"""

from os import path, listdir, remove, getcwd
from subprocess import Popen
import logging

import PySimpleGUI as sg

import downloader as dl
import workout_finder as wf
import authorization as auth

logging.basicConfig(
    filename="data/debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bikes, days = True, 2
# Define the layout of the GUI
layout = [
    [sg.Button("Settings"), sg.Button("Manage Database")],
    [sg.Text("Choose an option to rank the workout:")],
    [sg.Radio("Peak Power", "RADIO1", key="Peak Power")],
    [sg.Radio("1 Minute", "RADIO1", key="1 Minute")],
    [sg.Radio("1km", "RADIO1", key="1km")],
    [sg.Radio("2km", "RADIO1", key="2km")],
    [sg.Radio("6km", "RADIO1", key="6km")],
    [sg.Radio("Hour of Power", "RADIO1", key="Hour of Power")],
    [sg.Radio("4x1km", "RADIO1", key="4x1km")],
    [sg.Radio("3x6km", "RADIO1", key="3x6km")],
    [sg.Radio("3x12", "RADIO1", key="3x12")],
    [sg.Radio("3x30", "RADIO1", key="3x30")],
    [sg.Button("Run"), sg.Button("Log"), sg.Button("Exit")],
]


def open_settings():
    """Open the settings window and reads the values of the settings."""
    settings_layout = [
        [sg.Checkbox("Include Bikes", default=True, enable_events=True, key="-BIKES-")],
        [sg.Text("Days to include")],
        [
            sg.Slider(
                range=(1, 21),
                default_value=2,
                expand_x=True,
                enable_events=True,
                orientation="horizontal",
                key="-DAY-",
            )
        ],
        [sg.Button("Exit"), sg.Button("Clean")],
    ]

    settings_window = sg.Window(
        "Settings", settings_layout, icon="resources/VarsityV.ico"
    )

    while True:  # The Event Loop
        event, values = settings_window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        elif event == "Clean":
            for file in listdir(path.join(getcwd(), "strokes")):
                remove(path.join(getcwd(), "strokes", file))
            for file in listdir(path.join(getcwd(), "results")):
                remove(path.join(getcwd(), "results", file))
            clean = sg.Window(
                title="Clean-up",
                layout=[[sg.Text("Clean-up complete")], [sg.Button("Exit")]],
                icon="resources/VarsityV.ico",
            )
            while True:  # The Event Loops
                event, values = clean.read()
                print(event, values)
                if event == sg.WIN_CLOSED or event == "Exit":
                    break

            clean.close()

    settings_window.close()
    return (values["-BIKES-"] if values["-BIKES-"] is not None else True), (
        values["-DAY-"] - 1 if values["-DAY-"] is not None else 2
    )


# Create the window
window = sg.Window("Valkyrie", layout, icon="resources/VarsityV.ico")

# Write the event loop
while True:
    # Read the events and values from the window
    event, values = window.read()
    # If the user clicks the Exit button or closes the window, break the loop
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    # If the user clicks the Settings button, open the settings window
    elif event == "Settings":
        bikes, days = open_settings()

    elif event == "Manage Database":
        # Open the "Manage Databases" window as a persisting popup
        Popen(["python", "data_gui.py"])

    elif event == "Log":
        log = sg.Window(
            title="Log",
            layout=[
                [
                    sg.Text(
                        "Developed by Alexander Migus in consultation with Sascha Jansen-Rudan"
                    )
                ],
                [sg.Text("v2.0")],
                [sg.Text("  - First Release")],
                [sg.Text("  - Added PB support")],
                [sg.Text("  - Fixed stroke data bug")],
                [sg.Text("  - Fixed split bug")],
                [sg.Text("  - Changed xslx format to match Master Sheet")],
                [sg.Text("  - Changed name format to be Last, First")],
                [sg.Text("  - Improved split finding algorithm's efficiency")],
                [sg.Text("")],
                [sg.Text("v1.1")],
                [sg.Text("  - Tested in the erg room")],
                [sg.Text("  - Implemented GUI")],
                [sg.Text("  - Implemented Database")],
                [sg.Text("  - Implemented date filter")],
                [sg.Text("  - Added multiprocessing")],
                [sg.Text("")],
                [sg.Text("v1.0")],
                [sg.Text("  - Initial program")],
                [sg.Text("  - Tested using the Castle's profiles")],
                [sg.Button("Exit")],
            ],
            icon="resources/VarsityV.ico",
        )
        while True:  # The Event Loop
            event, values = log.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
        log.close()
    # If the user clicks the Run button, check which option is selected and run the API script
    elif event == "Run":
        if values["Peak Power"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.find_peak_power(api_token)
            wf.open_xlsx("peak_power")

        elif values["1 Minute"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.find_1min(bikes)
            wf.open_xlsx("1min")

        elif values["1km"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_single_distance(api_token, 200, 5, "1k", bikes)
            wf.open_xlsx("1k")

        elif values["2km"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            print("downloaded results")
            wf.rank_single_distance(api_token, 250, 8, "2k", bikes)
            wf.open_xlsx("2k")

        elif values["6km"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_single_distance(api_token, 500, 12, "6k", bikes)
            wf.open_xlsx("6k")

        elif values["Hour of Power"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_single_time(api_token, 3000, 12, "hour", bikes)
            wf.open_xlsx("hour")

        elif values["4x1km"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_intervals_distance(1000 * 4, 1000, 4, "4x1k", bikes)
            wf.open_xlsx("4x1k")

        elif values["3x6km"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_intervals_distance(6000 * 3, 6000, 3, "3x6k", bikes)
            wf.open_xlsx("3x6k")

        elif values["3x12"]:
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_intervals_time(7200, 3, "3x12min", bikes)
            wf.open_xlsx("3x12min")

        elif values["3x30"]:
            # Run the API script with option 10
            api_token = auth.auth()
            dl.get_results(api_token, days)
            wf.rank_intervals_time(18000, 3, "3x30min", bikes)
            wf.open_xlsx("3x30min")

        else:
            # No option is selected, show an error message
            sg.popup_error("Please select an option before running the script")

# Close the window
window.close()
