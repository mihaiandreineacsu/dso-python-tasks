"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import traceback
from init import init
from logger import log_msg
from utils import clean_metadata, log_metadata, run_subprocess


def metaclean_entrypoint():
    args = init()
    log_metadata(args)
    args.file = clean_metadata(args.file)
    log_metadata(args)


if __name__ == "__main__":
    try:
        metaclean_entrypoint()
    except Exception:
        log_msg(traceback.format_exc(), "ERROR")
