"""
    utils.datetime
    ~~~~~~~~~~~~~~

    Provide some time-related methods, cuz sometimes date and time in Python
    drive people crazy.
"""

import time


def get_current_timestamp():
    return int(time.time() * 1000)
