"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from logger import log_msg


def nmap_entrypoint():
    try:
        args = init()
    except Exception as e:
        log_msg(f"{e}", "ERROR")



if __name__ == '__main__':
    nmap_entrypoint()