import converter as cv
import workout_finder as wf
import database_request as dr


def converter():
    """
    >>> cv.calculate_split(500, 1000)
    '0:25.0'
    >>> cv.split_to_watts('2:00.0')
    203
    >>> cv.split_to_watts("01:30.0")
    480
    >>> cv.time_to_real(300)
    '0:30.0'
    >>> cv.time_to_real(931)
    '1:33.1'
    >>> cv.watts_to_split(202.5)
    '2:00.0'
    >>> cv.watts_to_split(480.1)
    '1:30.0'
    >>> cv.format_name("Alexander Migus")
    'Migus, Alexander'
    >>> cv.format_name("Sacha Jansen Rudan")
    'Jansen Rudan, Sascha'
    >>>
    """
    return


def finder():
    """
    >>> wf.find_approx(90, 110, 90, 110, 100)
    100.0
    >>> wf.find_approx(90, 110, 90, 110, 95)
    95.0
    >>> wf.find_approx(90, 110, 80, 120, 100)
    100.0
    >>> wf.find_approx(90, 110, 80, 120, 95)
    90.0
    """
    return


def database():
    """
    >>> dr.get_name(1524007)
    'Alexander Migus'
    """
    return


if __name__ == "__main__":
    import doctest

    doctest.testmod()
