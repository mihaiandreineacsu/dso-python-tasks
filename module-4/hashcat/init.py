"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
import os
from enums import HashModes, AttackModes
from logger import log_msg


def init()-> argparse.Namespace:
    """
    Initializes and validates Command-line arguments.

    Accepted arguments:
        -m --mode:          (int) optional  default MD5 (0),
        -a --attack:        (int) optional  default Brute-Force Attack (0),
        -d --dictionary:    (str) required if Dictionary Attach is chosen,
        -c --characterset:  (str) optional if Brute-Force Attack is chosen, default [a-z],

    Accepted required mutually exclusive arguments:
        -h --hash:          (str) required if hashfile not given,
        -H --hashfile:      (str) required if hash not given,

    Usage examples:
        python hashcat -m 0 -a 1 -d somefilecontainingwords.txt -h somehashedtext
    """
    log_msg("Initializing Hashcat Clone...")

    parser = argparse.ArgumentParser(description='Hashcat Clone', add_help=False)

    # Manually add help argument
    parser.add_argument('-help', '--help', action='help', help='Show this help message and exit')
    parser.add_argument(
        '-m', '--mode', required=False, type=int, choices=HashModes.list(), default=HashModes.MD5,
        help='Hashmodes MD5 (0), SHA-1 (1), SHA-256 (2) and SHA-512 (3). Default MD5 (0)')
    parser.add_argument(
        '-a', '--attack', required=False, type=int, choices=AttackModes.list(), default=AttackModes.BRUTE_FORCE_ATTACK,
        help='Attack modes Brute-Force Attack (0) and Dictionary Attack (1). Default Brute-Force Attack (0)')
    parser.add_argument('-d', '--dictionary', type=str, help='Dictionary file for Dictionary attack')
    parser.add_argument('-c', '--characterset', type=str, default='[a-z]', help='Character set for Brute-Force attack')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-h', '--hash', type=str, help='Hash from direct input')
    group.add_argument('-H', '--hashfile', type=str, help='Hash from file')

    args = parser.parse_args()

    args.mode = HashModes(args.mode)
    args.attack = AttackModes(args.attack)

    if args.hashfile:
        if not os.path.exists(args.hashfile):
            parser.error(f"The Hash file {args.hashfile} does not exist.")
        if os.path.getsize(args.hashfile) == 0:
            parser.error(f"The Hash file {args.hashfile} is empty.")

    if args.attack == AttackModes.DICTIONARY_ATTACK and not args.dictionary:
        parser.error("Dictionary file must be provided for Dictionary attack")

    if args.dictionary:
        if not os.path.exists(args.dictionary):
            parser.error(f"The Dictionary file {args.dictionary} does not exist.")
        if os.path.getsize(args.dictionary) == 0:
            parser.error(f"The Dictionary file {args.dictionary} is empty.")

    return args