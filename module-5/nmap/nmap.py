"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from logger import log_msg
from utils import find_opened_ports


def nmap_entrypoint():
    args = init()
    find_opened_ports(args)


if __name__ == "__main__":
    try:
        nmap_entrypoint()
    except Exception as e:
        log_msg(f"{e}", "ERROR")
