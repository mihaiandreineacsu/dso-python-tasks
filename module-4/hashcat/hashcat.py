"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from utils import exec_attack


def hashcat_entrypoint():
    args = init()
    exec_attack(args)


if __name__ == '__main__':
    hashcat_entrypoint()