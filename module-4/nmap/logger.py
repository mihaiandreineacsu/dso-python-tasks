"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
from typing import Literal
import datetime


LoggerLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
ShowDebugMsg = False


def init_logger(args: argparse.Namespace):
    global ShowDebugMsg
    if args.debug:
        ShowDebugMsg = True


def log_msg(msg: str, level: LoggerLevel = "INFO", strftime="%Y-%m-%d %H:%M:%S.%f"):
    """
    Logs formatted messages.

    Usage examples:
        log_msg("my message")                       # [2024.08.07 17:27:36:12]    [INFO] [my message]
        log_msg("my error message", "ERROR")        # [2024.08.07 17:27:36:12]    [ERROR] [my error message]
        log_msg("my warning message", "WARNING")    # [2024.08.07 17:27:36:12]    [WARNING] [my error message]
        log_msg("my debug message", "DEBUG")        # [2024.08.07 17:27:36:12]    [DEBUG] [my error message]

    Args:
        msg (str): Message to be logged
        level (LoggerLevel): The type of logging msg. Default is "INFO"
        strftime (str): Format of current_time default %Y-%m-%d %H:%M:%S.%f
    """
    global ShowDebugMsg
    if not ShowDebugMsg and level == "DEBUG":
        return
    assert isinstance(msg, str), "msg must be a string"
    assert level in LoggerLevel.__args__, f"level must be one of {LoggerLevel.__args__}"

    current_time = datetime.datetime.now().strftime(strftime)
    print(f"[{current_time}]\t[{level}]\t[{msg}]")
