"""
This module provides functions for converting and formatting data.

Functions:
- calculate_split(time_tenths:int, distance_m:int) -> str: Calculates split for a distance and time
- split_to_watts(split:str) -> int: Converts split to watts using the formula watts = 2.80 / pace^3
- time_to_real(time:int) -> str: Converts a time in tenths of a second to a time in 'm:ss.f' format
- watts_to_split(watts:float) -> str: Converts watts to split time using pace = (2.8 / watts)^(1/3)
- format_name(name:str) -> str: Formats a name from 'First Last' to 'Last, First'
"""

def calculate_split(time_tenths:int, distance_m:int) -> str:
    """
    Calculates the split time for a given distance and time in tenths of a second, returns h:mm:ss.f
    """
    time_seconds = time_tenths / 10
    speed_ms = distance_m / time_seconds
    split_500m = 500 / speed_ms

    # Calculate minutes, seconds and tenths of seconds
    minutes = int(split_500m // 60)
    seconds = int(split_500m % 60)
    tenths = int((split_500m * 10) % 10)

    # Return split time in 'm:ss.f' format

    return f"{minutes}:{seconds:02}.{tenths}"


def split_to_watts(split:str) -> int:
    """
    Converts a split time to watts using the formula watts = 2.80 / pace^3.

    Args:
        split (str): The split time in 'm:ss.f' format

    Returns:
        int: The watts value
    """
    minutes, seconds = split.split(":")
    seconds = float(minutes) * 60 + float(seconds)
    pace = seconds / 500
    watts = 2.80 / pace**3
    return round(watts)


def time_to_real(time:int) -> str:
    """
    Converts a time in tenths of a second to a time in 'm:ss.f' format.

    Args:
        time (int): The time in tenths of a second

    Returns:
        str: The time in 'h:mm:ss.f' format
    """
    time = time / 10
    hours = int(time // 3600)
    minutes = int(time // 60)
    seconds = int(time % 60)
    tenths = int((time * 10) % 10)
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}.{tenths}"
    return f"{minutes}:{seconds:02}.{tenths}"


def watts_to_split(watts:float) -> str:
    """
    Converts watts to a split time using the formula pace = (2.8 / watts)^(1/3).

    Args:
        watts (float): The watts value

    Returns:
        str: The split time in 'm:ss.f' format
    """
    pace =  (2.8 / watts) ** (1 / 3)
    time = pace * 500
    return time_to_real(time*10)

def calculate_watts(time_tenths:int, distance_m:int) -> int:
    """
    Calculates the watts for a given distance and time in tenths of a second.

    Args:
        time_tenths (int): The time in tenths of a second
        distance_m (int): The distance in meters

    Returns:
        int: The watts value
    """
    return split_to_watts(calculate_split(time_tenths, distance_m))


def format_name(name:str) -> str:
    """
    Formats a name from 'First Last' to 'Last, First'.

    Args:
        name (str): The name in 'First Last' format

    Returns:
        str: The formatted name in 'Last, First' format
    """
    name = name.split()
    if len(name) == 3:
        return f"{name[1]} {name[2]}, {name[0]}"
    return f"{name[1]}, {name[0]}"
