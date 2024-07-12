"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
from enums import HashModes, AttackModes
from logger import log_msg


def init()-> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -m --mode:      (int) optional  default MD5 (0),
        -a --attack:    (int) optional  default Brute-Force Attack (0),

    Accepted required mutually exclusive arguments:
        -h --hash:      (str)
        -H --hashfile:  (str)

    Usage examples:

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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-h', '--hash', type=str, help='Hash from direct input')
    group.add_argument('-H', '--hashfile', type=str, help='Hash from file')

    args = parser.parse_args()

    args.mode = HashModes(args.mode)
    args.attack = AttackModes(args.attack)

    if args.attack == AttackModes.DICTIONARY_ATTACK and not args.dictionary:
        parser.error("Dictionary file must be provided for Dictionary attack")

    return args