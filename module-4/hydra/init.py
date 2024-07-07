"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse

def init()-> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -u --username: (str) required,
        -s --server: (str) required,
        -p --port: (int) default 22,
        -w --wordlist: (str),
        -c --characterset: (str) default [a-z],
        --min: (int) default 3,
        --max: (int) default 3

    Usage examples:
        Using wordlist: $python hydra.py -u mihaiandrei -s 127.0.0.1 -p 2222 -w dictionary.txt
        Using characterset: $python hydra.py -u mihaiandrei -s 127.0.0.1 -p 2222 -c [a-ZA-z0-9] --min 3 --max 4
    """
    print("Initializing Hydra Clone...")
    parser = argparse.ArgumentParser(description='Hydra Clone')

    parser.add_argument('-u', '--username', required=True, type=str, help='Username to connect')
    parser.add_argument('-s', '--server', required=True, type=str, help='Server as IP-Address or DNS name to connect')
    parser.add_argument('-p', '--port', required=False, type=int, default=22, help='SSH port. Default is 22')
    parser.add_argument('-w', '--wordlist', required=False, type=str, help='Word list file used as dictionary')
    parser.add_argument('-c', '--characterset', required=False, type=str, default='[a-z]', help='Basic characters set used to generate a list of words. Default is [a-z]')
    parser.add_argument('--min', required=False, type=int, default=3, help='Minimal generated word length. Default is 3')
    parser.add_argument('--max', required=False, type=int, default=3, help='Maximal generated word length. Default is 3')

    args = parser.parse_args()
    return args