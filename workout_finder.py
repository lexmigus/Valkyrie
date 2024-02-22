"""
This module contains functions for finding and analyzing workout data,
and saving the results to an Excel file.

Functions:
- output_to_xlsx(ranking: list, name: str, banner: list) -> None
- open_xlsx(name: str) -> None
- find_approx(dist1: float, dist2: float, time1: float, time2: float, target_distance: int) -> float
- get_intervals(workout_id: str, split_length: int, num_splits: int) -> list
- get_times(workout_id: str, split_length: int, num_splits: int) -> list
"""

import logging
import os
from json import load
from datetime import datetime, timedelta
from typing import List, Union

from openpyxl import Workbook
import PySimpleGUI as sg

import converter as cv
import database_request as dr
import downloader as dl

logging.basicConfig(
    filename="data/debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
JSON = os.path.join(os.getcwd(), "json")
STROKES = os.path.join(os.getcwd(), "strokes")
USERS = dr.get_number_users()
BANNERS = {
    "peak_power": ["Name", "PB", "Date", "Watts", "Split", "SPM"],
    "1min": ["Name", "PB", "Date", "Distance", "Split", "Watts", "SPM"],
    "1k": [
        "Name",
        "PB",
        "Date",
        "Time",
        "Avg Split",
        "Watts",
        "SPM",
        "200m",
        "400m",
        "600m",
        "800m",
        "1000m",
    ],
    "2k": [
        "Name",
        "PB",
        "Date",
        "Time",
        "Avg Split",
        "Watts",
        "SPM",
        "250m",
        "500m",
        "750m",
        "1000m",
        "1250m",
        "1500m",
        "1750m",
        "2000m",
    ],
    "6k": [
        "Name",
        "PB",
        "Date",
        "Time",
        "Avg Split",
        "Watts",
        "SPM",
        "500m",
        "1000m",
        "1500m",
        "2000m",
        "2500m",
        "3000m",
        "3500m",
        "4000m",
        "4500m",
        "5000m",
        "5500m",
        "6000m",
    ],
    "hour": [
        "Name",
        "PB",
        "Date",
        "Distance",
        "Avg Split",
        "Watts",
        "SPM",
        "250m",
        "500m",
        "750m",
        "1000m",
        "1250m",
        "1500m",
        "1750m",
        "2000m",
    ],
    "4x1k": [
        "Name",
        "PB",
        "Date",
        "AVG Split",
        "Watts",
        "SPM",
        "Split 1",
        "Split 2",
        "Split 3",
        "Split 4",
    ],
    "3x6k": [
        "Name",
        "PB",
        "Date",
        "AVG Split",
        "Watts",
        "SPM",
        "Split 1",
        "Split 2",
        "Split 3",
    ],
    "3x12min": [
        "Name",
        "PB",
        "Date",
        "AVG Split",
        "Watts",
        "SPM",
        "Split 1",
        "Split 2",
        "Split 3",
    ],
    "3x30min": [
        "Name",
        "PB",
        "Date",
        "AVG Split",
        "Watts",
        "SPM",
        "Split 1",
        "Split 2",
        "Split 3",
    ],
}
BIKE_DISTANCE_FACTOR = 2
SECONDS_PER_MINUTE = 60
TENTHS_PER_MINUTE = 600
DATE_CONSTANT = 10


def output_to_xlsx(ranking: list, name: str, banner: list) -> None:
    """
    Output the ranking data to an Excel file.

    Args:
        ranking (list): The ranking data.
        name (str): The name of the Excel file.
        banner (list): The header row for the ranking data.

    Returns:
        None
    """
    if os.path.exists(name):
        os.chmod(name, 0o777)
    wb = Workbook()
    ws = wb.active
    ws.append(banner)
    for row in ranking:
        ws.append(row)

    wb.save(name)

    os.chmod(name, 0o777)

    print("File saved successfully")


def open_xlsx(name: str) -> None:
    """
    Open the Excel file.

    Args:
        name (str): The name of the Excel file.

    Returns:
        None
    """
    os.chdir("results")
    os.startfile(str(datetime.today().strftime("%Y-%m-%d")) + "_" + name + ".xlsx")
    os.chdir("..")


def find_approx(
    distance1: float, distance2: float, time1: float, time2: float, target_distance: int
) -> float:
    """
    Find the approximate time for a target distance based on two known distances and times.

    Args:
        distance1 (float): The first known distance.
        distance2 (float): The second known distance.
        time1 (float): The time for the first known distance.
        time2 (float): The time for the second known distance.
        target_distance (int): The target distance.

    Returns:
        float: The approximate time for the target distance.
    """
    percentage = (target_distance * 10 - distance1) / (distance2 - distance1)
    approx_time = time1 + (time2 - time1) * percentage
    return approx_time


def get_intervals(workout_id: str, split_length: int, num_splits: int) -> list:
    """
    Get the split times for a given workout ID.

    Args:
        id (str): The workout ID.
        split_length (int): The length of each split.
        num_splits (int): The number of splits to retrieve.

    Returns:
        list: The split times and the accumulated time.
    """
    try:
        file_path = os.path.join(STROKES, str(workout_id) + ".json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = load(f)
        splits = []
        target = split_length
        accumulated_time = 0
        for num, stroke in enumerate(data["data"]):
            stroke = data["data"][num]
            if stroke["d"] == target * 10:
                splits.append(
                    cv.calculate_split(stroke["t"] - accumulated_time, split_length)
                )
                accumulated_time = stroke["t"]
                if len(splits) == num_splits:
                    return splits, accumulated_time
                target += split_length

            elif stroke["d"] > target * 10:
                previous = data["data"][num - 1]
                split_time = find_approx(
                    previous["d"],
                    stroke["d"],
                    previous["t"],
                    stroke["t"],
                    target,
                )
                splits.append(
                    cv.calculate_split(split_time - accumulated_time, split_length)
                )
                accumulated_time = split_time
                if len(splits) == num_splits:
                    return splits, accumulated_time
                target += split_length
    except KeyError as e:
        logging.error(e)


def get_times(workout_id: str, split_length: int, num_splits: int) -> list:
    """
    Get the split distances for a given workout ID.

    Args:
        id (str): The workout ID.
        split_length (int): The length of each split.
        num_splits (int): The number of splits to retrieve.

    Returns:
        list: The split distances and the accumulated distance.
    """
    try:
        file_path = os.path.join(STROKES, str(workout_id) + ".json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = load(f)
        splits = []
        found = 0
        target = split_length
        accumulated_dist = 0
        for num, stroke in enumerate(data["data"]):
            stroke = data["data"][num]
            if stroke["d"] == target:
                splits.append(
                    cv.calculate_split(split_length, stroke["d"] - accumulated_dist)
                )
                found += 1
                accumulated_dist = stroke["d"]
                if len(splits) == num_splits:
                    return splits, accumulated_dist
                target += split_length

            elif stroke["d"] > target * 10:
                previous = data["data"][num - 1]
                split_dist = find_approx(
                    previous["t"],
                    stroke["t"],
                    previous["d"],
                    stroke["d"],
                    target,
                )
                found += 1
                splits.append(
                    cv.calculate_split(split_length, split_dist - accumulated_dist)
                )
                accumulated_dist = split_dist
                if len(splits) == num_splits:
                    return splits, accumulated_dist
                target += split_length
    except KeyError as e:
        logging.error(e)


def process_workout(
    workout: dict, category: str, is_interval=False
) -> List[Union[str, int]]:
    """
    Processes an individual workout and returns information about it.

    Args:
        workout (dict): The workout dictionary containing information about the workout.
        category (str): The type of information to return ("time" or "distance").
        is_interval (bool, optional): Whether the workout is an interval workout. Defaults to False.

    Returns:
        List[Union[str, int]]: A list of information about the workout.

    """
    dist = (
        workout["distance"]
        if workout["type"] == "rower"
        else workout["distance"] / BIKE_DISTANCE_FACTOR
    )
    info = [
        cv.format_name(dr.get_name(workout["user_id"])),
        "bike" if workout["type"] == "bike" else "",
        workout["date"][:10],
        (
            workout["distance"]
            if category == "time"
            else cv.time_to_real(workout["time"])
        ),
        cv.calculate_split(workout["time"], dist),
        cv.calculate_watts(workout["time"], dist),
        (
            workout["stroke_rate"]
            if "stroke_rate" in workout
            else (workout["stroke_count"] // (workout["time"] / TENTHS_PER_MINUTE))
        ),
    ]
    if is_interval:
        info.remove(info[3])
    return info


def find_peak_power(api_token: str) -> None:
    """
    Find the peak power for each user's workout and save the results to an Excel file.

    Args:
        api_token (str): The API token for authentication.

    Returns:
        None
    """
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        try:
            file_path = os.path.join(JSON, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = load(f)
            if "data" in data:
                maximum, spm = float("inf"), 0
                for result in data["data"]:
                    if result["distance"] <= 100:
                        dl.get_stroke_data(result["user_id"], result["id"], api_token)
                        path = os.path.join(STROKES, str(result["id"]) + ".json")
                        with open(path, "r", encoding="utf-8") as f:
                            piece = load(f)
                        for stroke in piece["data"]:
                            if stroke["p"] < maximum:
                                maximum, spm = stroke["p"], stroke["spm"]

                        if maximum not in [float("inf"), 0]:
                            ranking.append(
                                [
                                    cv.format_name(dr.get_name(result["user_id"])),
                                    "",
                                    result["date"][:10],
                                    cv.split_to_watts(cv.time_to_real(maximum)),
                                    cv.time_to_real(maximum),
                                    spm,
                                ]
                            )
                            window["progress"].update(i + 1)
        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)
    ranking.sort(key=lambda x: x[2], reverse=True)

    output_to_xlsx(
        ranking,
        (f'results/{str(datetime.today().strftime("%Y-%m-%d"))}_peak_power.xlsx'),
        BANNERS["peak_power"],
    )
    window.close()


def find_1min(bikes: bool) -> None:
    """
    Find the 1-minute ranking for each user's workout and save the results to an Excel file.

    Args:
        bikes (bool): Flag indicating whether to include bike workouts.

    Returns:
        None
    """
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        file_path = os.path.join(JSON, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = load(f)

        try:
            if "data" in data:
                for result in data["data"]:
                    if (
                        result["workout_type"] == "FixedTimeSplit"
                        and result["time"] == 600
                        and (result["type"] == "rower" if not bikes else True)
                    ):
                        ranking += process_workout(result, "time")

                        window["progress"].update(i + 1)
        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)

    ranking.sort(key=lambda x: (x[1] != "bike", x[3]))

    output_to_xlsx(
        ranking,
        (f'results/{str(datetime.today().strftime("%Y-%m-%d"))}_1min.xlsx'),
        BANNERS["1min"],
    )
    window.close()


def rank_single_distance(
    api_token: str,
    split_length: int,
    num_intervals: int,
    workout_name: str,
    bikes: bool = False,
) -> None:
    """Rank the workouts for a single distance and save the results

    Args: api_token (str): The API token for authentication
    split_length (int): The length of each split
    num_intervals (int): The number of intervals
    workout_name (str): The name of the workout
    bikes (bool): Flag indicating whether to include bike workouts

    Returns: None"""
    logging.info("Ranking %s workout", workout_name)
    distance = split_length * num_intervals
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        try:
            file_path = os.path.join(JSON, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = load(f)
            for result in data["data"]:
                dist = (
                    result["distance"]
                    if result["type"] == "rower"
                    else result["distance"] / BIKE_DISTANCE_FACTOR
                )
                if (
                    result["workout_type"] == "FixedDistanceSplits"
                    and dist == distance
                    and result["type"] == "rower"
                    and (result["type"] == "rower" if not bikes else True)
                ):

                    rank = process_workout(result, "distance")

                    dl.get_stroke_data(result["user_id"], result["id"], api_token)
                    splits, accumulated = get_intervals(
                        result["id"], split_length, num_intervals - 1
                    )
                    splits.append(
                        cv.calculate_split(result["time"] - accumulated, split_length)
                    )

                    rank += splits
                    ranking.append(rank)
                    window["progress"].update(i + 1)

        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)
    window.close()

    ranking.sort(key=lambda x: (x[1] != "bike", x[3]))

    output_to_xlsx(
        ranking,
        (f"results/{str(datetime.today().strftime('%Y-%m-%d'))}_{workout_name}.xlsx"),
        BANNERS[workout_name],
    )
    window.close()


def rank_single_time(
    api_token: str,
    time: int,
    split_length: int,
    num_intervals: int,
    workout_name: str,
) -> None:
    """Rank the workouts for a single time interval and save the results"""
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        try:
            file_path = os.path.join(JSON, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = load(f)
            if "data" in data:
                for result in data["data"]:
                    if (
                        result["workout_type"] == "FixedTimeSplits"
                        and result["time"] == time
                    ):
                        rank = process_workout(result, "time")

                        dl.get_stroke_data(result["user_id"], result["id"], api_token)
                        splits, accumulated = get_times(
                            result["id"], split_length, num_intervals - 1
                        )
                        splits.append(
                            cv.calculate_split(
                                split_length, result["distance"] - accumulated
                            )
                        )
                        rank += splits
                        ranking.append(rank)
                        window["progress"].update(i + 1)

        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)
    window.close()

    ranking.sort(key=lambda x: (x[1] != "bike", x[3]))

    output_to_xlsx(
        ranking,
        (f"results/{str(datetime.today().strftime('%Y-%m-%d'))}_{workout_name}.xlsx"),
        BANNERS[workout_name],
    )
    window.close()


def rank_intervals_distance(
    dist: int, interval_length: int, num_intervals: int, workout_name: str, bikes: bool
) -> None:
    """Rank the workouts for a distance with intervals and save the results.

    Args:
        dist (int): The distance of the workout
        interval_length (int): The length of each interval
        num_intervals (int): The number of intervals
        workout_name (str): The name of the workout
        bikes (bool): Flag indicating whether to include bike workouts

    Returns: None"""
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        file_path = os.path.join(JSON, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = load(f)

        try:
            if "data" in data:
                for result in data["data"]:
                    if (
                        (
                            (
                                result["workout_type"] == "FixedTimeInterval"
                                or result["workout_type"] == "VariableInterval"
                            )
                            and result["distance"] == dist
                        )
                        or (
                            bikes
                            and result["workout_type"] == "FixedTimeInterval"
                            or bikes
                            and result["workout_type"] == "VariableInterval"
                        )
                        and result["distance"] == dist * 2
                    ):
                        rank = process_workout(result, "distance", is_interval=True)

                        for interval in range(num_intervals):
                            time = result["workout"]["intervals"][interval]["time"]
                            if result["type"] == "bike":
                                time /= BIKE_DISTANCE_FACTOR
                            rank.append(
                                cv.calculate_split(
                                    result["workout"]["intervals"][interval]["time"],
                                    interval_length,
                                )
                            )
                        ranking.append(rank)
                        window["progress"].update(i + 1)

        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)

    ranking.sort(key=lambda x: (x[1] != "bike", x[3]))

    output_to_xlsx(
        ranking,
        (f'results/{str(datetime.today().strftime("%Y-%m-%d"))}_{workout_name}.xlsx'),
        BANNERS[workout_name],
    )
    window.close()


def rank_intervals_time(
    interval_length: int, num_intervals: int, workout_name: str, bikes: bool
) -> None:
    """Rank the workouts for a time workout with intervals and save the results.

    Args:
        interval_length (int): The length of each interval
        num_intervals (int): The number of intervals
        workout_name (str): The name of the workout
        bikes (bool): Flag indicating whether to include bike workouts

    Returns: None"""
    time = interval_length * num_intervals
    ranking = []
    layout = [
        [sg.Text("Ranking workouts...")],
        [sg.ProgressBar(USERS, orientation="h", size=(20, 20), key="progress")],
    ]
    window = sg.Window(
        "Progress Bar", layout, finalize=True, icon="resources/VarsityV.ico"
    )

    for i, filename in enumerate(os.listdir(JSON)):
        file_path = os.path.join(JSON, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = load(f)
        try:
            if "data" in data:
                for result in data["data"]:
                    if (
                        (
                            result["workout_type"] == "FixedTimeInterval"
                            or result["workout_type"] == "VariableInterval"
                        )
                        and result["time"] == time
                        and (result["type"] == "rower" if not bikes else True)
                    ):

                        rank = process_workout(result, "time", is_interval=True)

                        for interval in range(num_intervals):
                            dist = result["workout"]["intervals"][interval]["distance"]
                            if result["type"] == "bike":
                                dist /= BIKE_DISTANCE_FACTOR
                            rank.append(
                                cv.calculate_split(
                                    interval_length,
                                    dist,
                                )
                            )

                        ranking.append(rank)
                        window["progress"].update(i + 1)

        except KeyError as e:
            logging.error(e)
            window["progress"].update(i + 1)

    ranking.sort(key=lambda x: (x[1] != "bike", x[3]))

    output_to_xlsx(
        ranking,
        (f'results/{str(datetime.today().strftime("%Y-%m-%d"))}_{workout_name}.xlsx'),
        BANNERS[workout_name],
    )
    window.close()


if __name__ == "__main__":
    ID10T = sg.Window(
        title="Error ID10T",
        layout=[[sg.Text("Dumbass")], [sg.Button("Resign to your repeated failure")]],
        icon="resources/error.ico",
    )
    while True:  # The Event Loop
        event, values = ID10T.read()
        if event == sg.WIN_CLOSED or event == "Resign to your repeated failure":
            break

    ID10T.close()
