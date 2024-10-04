"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from utils import exec_connections


def hydra_entrypoint():
    args = init()
    exec_connections(args)


if __name__ == "__main__":
    hydra_entrypoint()
